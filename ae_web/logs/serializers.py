from pinax.eventlog.models import Log
from rest_framework import serializers

__author__ = 'Ahmed G. Ali'


class LogSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Log
        fields = ('user', 'timestamp', 'action', 'object_id', 'extra')
