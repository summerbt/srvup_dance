# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0007_auto_20150920_2353'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'\nLearn to dance!\n'),
            preserve_default=True,
        ),
    ]
