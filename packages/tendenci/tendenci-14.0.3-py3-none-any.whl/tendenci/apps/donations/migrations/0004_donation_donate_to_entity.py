# Generated by Django 2.2.24 on 2021-06-17 17:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0005_entity_show_for_donation'),
        ('donations', '0003_auto_20200902_1545'),
    ]

    operations = [
        migrations.AddField(
            model_name='donation',
            name='donate_to_entity',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='entities.Entity'),
        ),
    ]
