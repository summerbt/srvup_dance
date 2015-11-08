# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0008_video_share_message'),
    ]

    operations = [
        migrations.AlterField(
            model_name='video',
            name='share_message',
            field=models.TextField(default=b'\nCheck out this awesome video!\n'),
            preserve_default=True,
        ),
    ]
