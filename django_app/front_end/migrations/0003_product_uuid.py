# Generated by Django 4.1.2 on 2022-10-25 20:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("front_end", "0002_purchasedmovies"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("760846d9-9629-4c9c-a378-5daa90a42d01"),
            ),
        ),
    ]
