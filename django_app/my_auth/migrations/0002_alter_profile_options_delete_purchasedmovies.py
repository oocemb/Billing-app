# Generated by Django 4.1.2 on 2022-10-16 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("my_auth", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="profile",
            options={
                "verbose_name": "Профиль пользователя",
                "verbose_name_plural": "Профили пользователей",
            },
        ),
        migrations.DeleteModel(
            name="PurchasedMovies",
        ),
    ]