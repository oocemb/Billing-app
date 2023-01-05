# Generated by Django 4.1.2 on 2022-11-07 19:06

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("front_end", "0005_plansubscriptionmovie_uuid_alter_product_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plansubscriptionmovie",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("21808bc5-aad0-4a2b-9687-273c2e4e825c")
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="uuid",
            field=models.UUIDField(
                auto_created=True,
                default=uuid.UUID("19423a2e-91e1-46b9-9989-248c9203290f"),
            ),
        ),
    ]