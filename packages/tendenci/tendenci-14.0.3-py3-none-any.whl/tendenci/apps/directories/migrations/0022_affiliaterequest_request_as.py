# Generated by Django 2.2.18 on 2021-02-22 22:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('directories', '0021_auto_20210209_1540'),
    ]

    operations = [
        migrations.AddField(
            model_name='affiliaterequest',
            name='request_as',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='affiliate_requests', to='directories.Category'),
        ),
        migrations.AddField(
            model_name='affiliateship',
            name='connected_as',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cat_affiliateships', to='directories.Category'),
        ),
    ]
