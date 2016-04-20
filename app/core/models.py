from __future__ import unicode_literals

from django.db import models


# Create your models here.
class BaseModel(models.Model):
    is_active = models.BooleanField(default=True)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

"""
#
# AdsModel(info)
#
"""


class AdsModel(BaseModel):
    name = models.CharField("Name", max_length=500, blank=True, null=True)
    description = models.TextField('Description', blank=True, null=True)
