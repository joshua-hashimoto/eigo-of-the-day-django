# Generated by Django 3.1 on 2020-08-04 15:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('eigo', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='example',
            name='memo',
        ),
        migrations.RemoveField(
            model_name='phrase',
            name='memo',
        ),
    ]
