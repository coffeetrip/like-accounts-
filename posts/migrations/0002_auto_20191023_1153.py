# Generated by Django 2.2.4 on 2019-10-23 02:53

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(upload_to='feeds'),
        ),
    ]
