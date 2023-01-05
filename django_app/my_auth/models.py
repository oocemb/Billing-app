import uuid
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from front_end.models import PlanSubscriptionMovie


class Profile(models.Model):

    class StatusSubscribe(models.TextChoices):
        ENABLE = "enable", "enable"
        DISABLE = "disable", "disable"
        CANCEL = "cancel", "cancel"

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(auto_created=True, default=uuid.uuid4)
    subscription_plan = models.ForeignKey(
        PlanSubscriptionMovie,
        blank=True,
        null=True,
        default=None,
        on_delete=models.SET_DEFAULT,
    )
    subscription_status = models.CharField(
        "status",
        max_length=8,
        choices=StatusSubscribe.choices,
        default=StatusSubscribe.ENABLE,
    )
    avatar = models.ImageField(
        upload_to="static/img/avatars/",
        blank=True,
        null=True,
        default="static/img/content/avatar-9.jpg",
    )
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    subscription_last_payment_date = models.DateField(
        blank=True, null=True, default=None
    )

    class Meta:
        verbose_name = "Профиль пользователя"
        verbose_name_plural = "Профили пользователей"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
