# Generated by Django 4.1.2 on 2022-10-16 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PlanSubscriptionMovie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
            options={
                "verbose_name": "Ценовой уровень подписки",
                "verbose_name_plural": "Ценовые уровни подписок",
            },
        ),
        migrations.CreateModel(
            name="ProductCategory",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default=None, max_length=64, null=True
                    ),
                ),
                (
                    "image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="static/img/category_images/",
                    ),
                ),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
            ],
            options={
                "verbose_name": "Категория фильмов",
                "verbose_name_plural": "Категории фильмов",
            },
        ),
        migrations.CreateModel(
            name="TierPriceMovie",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(blank=True, max_length=64, null=True)),
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0, max_digits=10),
                ),
            ],
            options={
                "verbose_name": "Ценовой уровень фильмов",
                "verbose_name_plural": "Ценовые уровни фильмов",
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "imdb",
                    models.DecimalField(decimal_places=1, default=1.1, max_digits=3),
                ),
                (
                    "main_image",
                    models.ImageField(
                        blank=True,
                        default=None,
                        null=True,
                        upload_to="static/img/products_images/",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        blank=True, default=None, max_length=128, null=True
                    ),
                ),
                ("description", models.TextField(blank=True, default=None, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("updated", models.DateTimeField(auto_now=True)),
                ("category", models.ManyToManyField(to="front_end.productcategory")),
                (
                    "price_tier",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="front_end.tierpricemovie",
                    ),
                ),
                (
                    "subscription_plan",
                    models.ForeignKey(
                        blank=True,
                        default=None,
                        null=True,
                        on_delete=django.db.models.deletion.SET_DEFAULT,
                        to="front_end.plansubscriptionmovie",
                    ),
                ),
            ],
            options={
                "verbose_name": "Фильм",
                "verbose_name_plural": "Фильмы",
            },
        ),
    ]