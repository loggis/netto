# Generated by Django 3.1.2 on 2020-11-02 16:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('netto', '0006_setting'),
    ]

    operations = [
        migrations.RenameField(
            model_name='setting',
            old_name='prmts',
            new_name='time_sleep',
        ),
    ]
