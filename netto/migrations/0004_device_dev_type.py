# Generated by Django 3.1.2 on 2020-11-02 11:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('netto', '0003_auto_20201102_1814'),
    ]

    operations = [
        migrations.AddField(
            model_name='device',
            name='dev_type',
            field=models.CharField(blank=True, choices=[('router', 'Router'), ('switch', 'Switch')], max_length=255),
        ),
    ]
