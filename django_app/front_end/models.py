import uuid

from django.db import models
from django.contrib.auth.models import User


class TierPriceMovie(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)

    def __str__(self) -> str:
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Ценовой уровень фильмов"
        verbose_name_plural = "Ценовые уровни фильмов"


class PlanSubscriptionMovie(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4())
    name = models.CharField(max_length=64, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0)
    quality = models.CharField(max_length=64, blank=True, null=True)
    device = models.CharField(max_length=64, blank=True, null=True)

    def __str__(self) -> str:
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Ценовой уровень подписки"
        verbose_name_plural = "Ценовые уровни подписок"


class ProductCategory(models.Model):
    name = models.CharField(max_length=64, blank=True, null=True, default=None)
    image = models.ImageField(
        upload_to="static/img/category_images/", blank=True, null=True, default=None
    )
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Категория фильмов"
        verbose_name_plural = "Категории фильмов"


class Product(models.Model):
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4())
    category = models.ManyToManyField(ProductCategory)
    price_tier = models.ForeignKey(
        TierPriceMovie,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    subscription_plan = models.ForeignKey(
        PlanSubscriptionMovie,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    imdb = models.DecimalField(max_digits=3, decimal_places=1, default=1.1)
    main_image = models.ImageField(
        upload_to="static/img/products_images/", blank=True, null=True, default=None
    )
    name = models.CharField(max_length=128, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now_add=False, auto_now=True)

    def __str__(self) -> str:
        return "%s" % (self.name)

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"


class PurchasedMovies(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie_id = models.ForeignKey(
        Product, blank=True, null=True, on_delete=models.SET_NULL
    )
    # status = models.

    class Meta:
        verbose_name = "Купленный фильм"
        verbose_name_plural = "Купленные фильмы"
