# Generated by Django 4.2 on 2023-04-21 11:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_media', '0002_alter_userprofile_mobile_number_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
    ]
