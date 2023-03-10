# Generated by Django 4.1.2 on 2022-11-07 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("my_auth", "0006_alter_profile_uuid"),
    ]

    operations = [
        migrations.AddField(
            model_name="profile",
            name="subscription_status",
            field=models.CharField(
                choices=[
                    ("enable", "enable"),
                    ("disable", "disable"),
                    ("cancel", "cancel"),
                ],
                default="enable",
                max_length=8,
                verbose_name="status",
            ),
        ),
        migrations.AlterField(
            model_name="profile",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("631e5d78-a3c9-4301-8fc6-d98c0eef3714"),
            ),
        ),
    ]
