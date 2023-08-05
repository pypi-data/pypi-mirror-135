# Generated by Django 2.2.20 on 2021-05-03 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0014_auto_20210224_0954'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrationconfiguration',
            name='reply_to',
            field=models.EmailField(verbose_name='Registration email reply to', blank=True, help_text='The email address that receives the reply message when registrants reply their registration confirmation emails.', max_length=120, null=True),
        ),
    ]
