# Generated by Django 4.1.2 on 2022-10-28 19:48

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("my_auth", "0004_alter_profile_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("ad028493-8a81-4eab-b88d-a1d343aa9401"),
            ),
        ),
    ]
