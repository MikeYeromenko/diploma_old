# Generated by Django 3.0.7 on 2020-06-14 10:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('seance', '0004_auto_20200613_1558'),
    ]

    operations = [
        migrations.AddField(
            model_name='advuser',
            name='was_deleted',
            field=models.BooleanField(default=False, verbose_name='was deleted?'),
        ),
        migrations.AlterField(
            model_name='film',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='instance created by'),
        ),
        migrations.AlterField(
            model_name='film',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='instance created at'),
        ),
        migrations.AlterField(
            model_name='film',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='in run?'),
        ),
        migrations.AlterField(
            model_name='film',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='instance updated at'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='halls', to=settings.AUTH_USER_MODEL, verbose_name='instance created by'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='instance created at'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='in run?'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='size',
            field=models.PositiveIntegerField(verbose_name='how many seats?'),
        ),
        migrations.AlterField(
            model_name='hall',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='instance updated at'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='admin',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='instance created by'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='instance created at'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='date_ends',
            field=models.DateField(blank=True, null=True, verbose_name='ends'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='in run?'),
        ),
        migrations.AlterField(
            model_name='seance',
            name='time_ends',
            field=models.TimeField(blank=True, null=True, verbose_name='ends at: '),
        ),
        migrations.AlterField(
            model_name='seance',
            name='updated',
            field=models.DateTimeField(auto_now=True, verbose_name='instance updated at'),
        ),
    ]
