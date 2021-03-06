# Generated by Django 3.0.1 on 2020-01-01 22:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycore', '0004_auto_20200101_2201'),
    ]

    operations = [
        migrations.AlterField(
            model_name='journal',
            name='key_in_date',
            field=models.DateTimeField(db_index=True, verbose_name='Date and time check-in'),
        ),
        migrations.AlterField(
            model_name='journal',
            name='key_out_date',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='Date and time check-out'),
        ),
        migrations.AlterField(
            model_name='room',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='mycore.Tenant'),
        ),
    ]
