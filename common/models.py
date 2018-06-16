from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin


class ContactType(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Contact(SoftDeleteMixin, models.Model):
    type = models.ForeignKey(ContactType, on_delete=models.PROTECT, )
    information = models.CharField(max_length=100, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class MediaType(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Media(SoftDeleteMixin, models.Model):
    type = models.ForeignKey(MediaType, on_delete=models.PROTECT, )
    url = models.URLField(max_length=500, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Ability(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=30, unique=True)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Keyword(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=30, unique=True)
    count = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )