from django.contrib import admin
from .models import (
    Product,
    ProductCategory,
    PlanSubscriptionMovie,
    TierPriceMovie,
    PurchasedMovies,
)


class ProductAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Product._meta.fields]

    class Meta:
        model = Product


admin.site.register(Product, ProductAdmin)


class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = [field.name for field in ProductCategory._meta.fields]

    class Meta:
        model = ProductCategory


admin.site.register(ProductCategory, ProductCategoryAdmin)


class PlanSubscriptionMovieAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PlanSubscriptionMovie._meta.fields]

    class Meta:
        model = PlanSubscriptionMovie


admin.site.register(PlanSubscriptionMovie, PlanSubscriptionMovieAdmin)


class TierPriceMovieAdmin(admin.ModelAdmin):
    list_display = [field.name for field in TierPriceMovie._meta.fields]

    class Meta:
        model = TierPriceMovie


admin.site.register(TierPriceMovie, TierPriceMovieAdmin)


class PurchasedMoviesAdmin(admin.ModelAdmin):
    list_display = [field.name for field in PurchasedMovies._meta.fields]

    class Meta:
        model = PurchasedMovies


admin.site.register(PurchasedMovies, PurchasedMoviesAdmin)
