# Generated by Django 3.1 on 2020-08-06 16:55

from django.db import migrations, models
import eigo.models


class Migration(migrations.Migration):

    dependencies = [
        ('eigo', '0005_auto_20200806_0423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='snap',
            name='snap',
            field=models.ImageField(upload_to=eigo.models.upload_image_to),
        ),
    ]
