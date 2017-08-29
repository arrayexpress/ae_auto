# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('maintenance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='validate',
            name='pubmed',
        ),
        migrations.AlterField(
            model_name='validate',
            name='status',
            field=models.CharField(default=b'P', max_length=1, choices=[(b'P', b'Pending'), (b'F', b'Finished'), (b'E', b'Execution Error')]),
        ),
        migrations.AlterField(
            model_name='validate',
            name='validation_report',
            field=models.TextField(null=True),
        ),
    ]
