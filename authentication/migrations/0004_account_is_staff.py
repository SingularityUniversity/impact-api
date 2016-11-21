# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_account_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='account',
            name='is_staff',
            field=models.BooleanField(default=False),
        ),
    ]
