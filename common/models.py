from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin


class ContactType(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Contact(SoftDeleteMixin, models.Model):
    pass


class MediaType(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Media(SoftDeleteMixin, models.Model):
    pass