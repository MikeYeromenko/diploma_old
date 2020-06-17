# Generated by Django 3.0.7 on 2020-06-17 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hall',
            name='size',
        ),
        migrations.AddField(
            model_name='hall',
            name='rows',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='how many seats?'),
        ),
        migrations.AddField(
            model_name='hall',
            name='seats',
            field=models.PositiveSmallIntegerField(default=0, verbose_name='how many seats?'),
        ),
    ]