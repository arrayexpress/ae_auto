from django.shortcuts import render

# Create your views here.
from pinax.eventlog.models import Log
from rest_framework import generics, permissions
from logs.serializers import LogSerializer


class LogListView(generics.ListCreateAPIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Log.objects.all()
    serializer_class = LogSerializer
    lookup_field = 'pk'


class LogDetail(generics.RetrieveUpdateDestroyAPIView):
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Log.objects.all()
    # model = models.Publication
    serializer_class = LogSerializer
    lookup_field = 'pk'