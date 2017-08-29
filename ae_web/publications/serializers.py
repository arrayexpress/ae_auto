import json

from rest_framework import serializers
from rest_framework.fields import Field, CharField, DictField, SerializerMethodField, IntegerField
from publications import models

__author__ = 'Ahmed G. Ali'


class PublicationSerializer(serializers.HyperlinkedModelSerializer):
    experiments = serializers.StringRelatedField(many=True, source='experiment_set', read_only=True)

    class Meta:
        model = models.Publication


class ExperimentSerializer(serializers.HyperlinkedModelSerializer):
    # publications = PublicationSerializer(many=True, read_only=True)
    # publications = serializers.StringRelatedField(many=True)

    publications = serializers.StringRelatedField(many=True,source='publication_set', read_only=True)

    # def __init__(self, *args, **kwargs):
    #     remove_fields = kwargs.pop('remove_fields', None)
    #     super(ExperimentSerializer, self).__init__(*args, **kwargs)
    #     if remove_fields:
    #         for field_name in remove_fields:
    #             self.fields.pop(field_name)

    class Meta:
        model = models.Experiment


class AssociationSerializer(serializers.HyperlinkedModelSerializer):
    id = IntegerField(read_only=True)
    publication = DictField(source='publication.to_dict', read_only=True)
    experiment = DictField(source='experiment.to_dict', read_only=True)

    @property
    def get_publication(self, obj):
        return serializers.serialize('json', 'publication')

    @property
    def get_experiment(self, obj):
        return serializers.serialize('json', 'experiment')


    # experiment = serializers.StringRelatedField( many=False, read_only=False)
    ass_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.Association
        read_only_fields = ('publication', 'experiment')
