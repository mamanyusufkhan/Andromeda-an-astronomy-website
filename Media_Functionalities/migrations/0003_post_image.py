# Generated by Django 3.2.7 on 2022-03-01 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Media_Functionalities', '0002_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='social/post_photos'),
        ),
    ]