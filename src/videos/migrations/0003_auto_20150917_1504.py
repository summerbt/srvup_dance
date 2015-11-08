# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0002_auto_20150913_2022'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='active',
            field=models.BooleanField(default=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='featured',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='video',
            name='free_preview',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
