from django.contrib import admin
from .models import Profile


class ProfileAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Profile._meta.fields]

    class Meta:
        model = Profile


admin.site.register(Profile, ProfileAdmin)
