# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Association',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('is_associated', models.BooleanField(default=0)),
                ('status', models.CharField(default=b'N', max_length=1, choices=[(b'N', b'New'), (b'A', b'Approved'), (b'R', b'Rejected')])),
            ],
        ),
        migrations.CreateModel(
            name='Experiment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('accession', models.CharField(unique=True, max_length=25)),
                ('title', models.TextField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pmc_id', models.CharField(unique=True, max_length=200)),
                ('pubmed', models.IntegerField(unique=True, null=True)),
                ('doi', models.CharField(max_length=200, null=True)),
                ('title', models.TextField()),
                ('whole_article', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='experiment',
            name='publications',
            field=models.ManyToManyField(to='publications.Publication', through='publications.Association'),
        ),
        migrations.AddField(
            model_name='association',
            name='experiment',
            field=models.ForeignKey(related_name='experiment', to='publications.Experiment'),
        ),
        migrations.AddField(
            model_name='association',
            name='publication',
            field=models.ForeignKey(related_name='publication', to='publications.Publication'),
        ),
        migrations.AlterUniqueTogether(
            name='association',
            unique_together=set([('experiment', 'publication')]),
        ),
    ]
