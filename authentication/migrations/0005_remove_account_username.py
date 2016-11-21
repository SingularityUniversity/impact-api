# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_account_is_staff'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='username',
        ),
    ]
