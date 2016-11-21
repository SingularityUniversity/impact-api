# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_remove_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='username',
            field=models.CharField(default='test', unique=True, max_length=40),
            preserve_default=False,
        ),
    ]
