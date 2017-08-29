import json

from braces.views import JSONResponseMixin
from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic.base import View
from rest_framework import status, generics, permissions
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dal.oracle.ae2.publication import insert_publication,  retrieve_pub, delete_publication_by_id
from dal.oracle.ae2.study import retrieve_study_id_by_acc
from dal.oracle.ae2.study_publication import delete_study_publication, insert_study_publication, \
    retrieve_associations_by_publication_id
from dal.oracle.ae2.view_publications import retrieve_existing_publications_by_accession, retrieve_pub_id_by_doi
from publications import models
from publications.models import Association
from publications.serializers import PublicationSerializer, ExperimentSerializer, AssociationSerializer, \
    ExperimentSerializer, AssociationSerializer, PublicationSerializer
from pinax.eventlog.models import log, Log


class PublicationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = PublicationSerializer
    # publications = retrieve_existing_publications_by_accession(acc='E-GEOD-13161')

    queryset = models.Publication.objects.all()
    # queryset = PublicationSerializer(publications, many=True).data
    # def get_queryset(self):
    #     return self.serializer


class PublicationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Publication.objects.all()
    # model = models.Publication
    serializer_class = PublicationSerializer


class ExperimentDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Experiment.objects.all()
    serializer_class = ExperimentSerializer


class AssociationDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = models.Association.objects.all()
    serializer_class = AssociationSerializer


class ExperimentList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = ExperimentSerializer
    # publications = retrieve_existing_publications_by_accession(acc='E-GEOD-13161')
    queryset = models.Experiment.objects.all()
    # queryset = ExperimentSerializer(publications, many=True).data


class AssociationList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = AssociationSerializer

    def get_queryset(self):
        self.serializer_class = AssociationSerializer
        queryset = models.Association.objects.all()
        status = self.request.query_params.get('status', None)
        associated = self.request.query_params.get('associated', None)
        if associated:
            queryset = queryset.filter(is_associated=associated)
        if status:
            queryset = queryset.filter(status=status)

        return queryset


class EditPublication(JSONResponseMixin, View):

    def post(self, request):
        action = ''
        association_status = request.POST.get('status')
        as_id = request.POST.get('id')
        association = Association.objects.get(id=as_id)
        association.status = association_status
        association.is_associated = False
        if association_status == 'N' or association_status == 'R':
            exp = retrieve_study_id_by_acc(association.experiment.accession)[0]
            pub = retrieve_pub(acc=json.loads(association.publication.whole_article)['id'],
                               pubmed=association.publication.pubmed)
            action = 'Rejecting association.'
            if association_status == 'N':
                action = 'Reverting association to New.'

            if pub and len(pub) > 0:
                delete_study_publication(exp.id, pub[0].id)
                associations = retrieve_associations_by_publication_id(pub[0].id)
                if len(associations) ==0:
                    delete_publication_by_id(pub[0].id)

        elif association_status == 'A':
            action = 'Approved!'
            exp = retrieve_study_id_by_acc(association.experiment.accession)[0]
            pub = retrieve_pub(acc=json.loads(association.publication.whole_article)['id'],
                               pubmed=association.publication.pubmed)

            if not pub or len(pub) == 0:
                pub_id = insert_publication(json.loads(association.publication.whole_article))
            else:
                pub_id = pub[0].id
            insert_study_publication(exp.id, pub_id)

        association.save()
        log(
            user=request.user,
            action=action,
            obj=association,
            # extra={
            #     "title": foo.title
            # }
        )

        # logs = Log.objects.filter(object_id=association.id, content_type=ContentType.objects.get_for_model(Association))
        # print logs[0]
        return self.render_json_response({}, 200)
