# Generated by Django 4.2 on 2023-04-22 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        (
            "social_media",
            "0002_remove_userprofile_user_userprofile_username_and_more",
        ),
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="first_name",
        ),
        migrations.RemoveField(
            model_name="user",
            name="last_name",
        ),
        migrations.AddField(
            model_name="user",
            name="profile",
            field=models.OneToOneField(
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="social_media.userprofile",
            ),
        ),
    ]
