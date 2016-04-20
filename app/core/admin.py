from django.contrib import admin

# Register your models here.
from core.models import AdsModel


class AdsModeldmin(admin.ModelAdmin):
    search_fields = ['id', 'name']
    list_display = ('name', 'is_active', 'created')


admin.site.register(AdsModel, AdsModeldmin)
