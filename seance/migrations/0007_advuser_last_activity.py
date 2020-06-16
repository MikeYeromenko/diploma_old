# Generated by Django 3.0.7 on 2020-06-15 06:47

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0006_auto_20200614_1218'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='last_activity',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2020, 6, 15, 6, 47, 15, 500432, tzinfo=utc), null=True, verbose_name="user's last activity was: "),
        ),
    ]