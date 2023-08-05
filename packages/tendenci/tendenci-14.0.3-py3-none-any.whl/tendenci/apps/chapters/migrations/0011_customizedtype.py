# Generated by Django 3.2.5 on 2021-12-08 14:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('chapters', '0010_chaptermembershipfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomizedType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Set 0 for free membership.', max_digits=15, verbose_name='Price')),
                ('renewal_price', models.DecimalField(blank=True, decimal_places=2, default=0, help_text='Set 0 for free membership.', max_digits=15, null=True, verbose_name='Renewal Price')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chapters.chapter')),
                ('membership_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customized_types', to='chapters.chaptermembershiptype')),
            ],
            options={
                'unique_together': {('membership_type', 'chapter')},
            },
        ),
    ]
