from django.db import models
from base.mixins.timestamp import (
    AutoCreatedUpdatedMixin, SoftDeleteMixin,
)

class Location(AutoCreatedUpdatedMixin, SoftDeleteMixin):
    address_0 = models.CharField(max_length=20, )
    address_0_code = models.CharField(max_length=2, )
    address_1 = models.CharField(max_length=20, blank=True, )
    address_1_code = models.CharField(max_length=5, blank=True, )
    address_2 = models.CharField(max_length=20, blank=True, )
    address_2_code = models.CharField(max_length=9, blank=True, )