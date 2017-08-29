# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Validate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('job_id', models.CharField(unique=True, max_length=200)),
                ('pubmed', models.IntegerField(unique=True, null=True)),
                ('data_dir', models.CharField(max_length=200, null=True)),
                ('validation_report', models.TextField()),
                ('status', models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pending'), (b'V', b'All Valid'), (b'I', b'Validation Error'), (b'E', b'Execution Error')])),
            ],
        ),
    ]
