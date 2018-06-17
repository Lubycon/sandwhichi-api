from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin

class Location(SoftDeleteMixin, models.Model):
    address_0 = models.CharField(max_length=20, )
    address_0_code = models.CharField(max_length=2, )
    address_1 = models.CharField(max_length=20, blank=True, )
    address_1_code = models.CharField(max_length=5, blank=True, )
    address_2 = models.CharField(max_length=20, blank=True, )
    address_2_code = models.CharField(max_length=9, blank=True, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )