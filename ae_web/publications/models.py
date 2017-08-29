import json

from django.core import serializers
from django.db import models
from django.db.models.fields.related import ManyToManyField
from django.forms import model_to_dict

ASSOCIATION_STATUS = (
    ('N', 'New'),
    ('A', 'Approved'),
    ('R', 'Rejected'),

)


class Publication(models.Model):
    pmc_id = models.CharField(null=False, unique=True, max_length=200)
    pubmed = models.IntegerField(unique=True, null=True)
    doi = models.CharField(null=True, max_length=200)
    title = models.TextField(null=False)
    whole_article = models.TextField(null=False)

    def __unicode__(self):
        # return u'%s(%s): %s' % (self.doi, str(self.pubmed), self.title,)
        return u'%s: %s' % (self.doi, self.title,)

    def to_dict(self):
        return model_to_dict(self)


class Experiment(models.Model):
    accession = models.CharField(max_length=25, unique=True)
    title = models.TextField(null=False)
    description = models.TextField(null=False)
    publications = models.ManyToManyField(Publication, through='Association')

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data

    def __unicode__(self):
        return json.dumps(self.to_dict())


class Association(models.Model):
    experiment = models.ForeignKey(Experiment, on_delete=models.CASCADE, related_name="experiment")
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name="publication")
    is_associated = models.BooleanField(default=0)
    status = models.CharField(max_length=1, choices=ASSOCIATION_STATUS, default='N')

    # id = models.IntegerField(auto_created=True, primary_key=True)

    class Meta:
        unique_together = ('experiment', 'publication')
