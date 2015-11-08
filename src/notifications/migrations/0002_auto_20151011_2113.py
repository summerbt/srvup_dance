# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0001_initial'),
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='action_content_type',
            field=models.ForeignKey(related_name='notify_acting_object', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='action_object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender_content_type',
            field=models.ForeignKey(related_name='notify_sending_object', default=0, to='contenttypes.ContentType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='sender_object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notification',
            name='target_content_type',
            field=models.ForeignKey(related_name='notify_targeted_object', blank=True, to='contenttypes.ContentType', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='notification',
            name='target_object_id',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
