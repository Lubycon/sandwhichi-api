# -*- coding: UTF-8 -*-

from django.db.models.query import QuerySet
from django.db import models
from django.utils.timezone import now

class SoftDeleteQuerySet(QuerySet):
    def delete(self):
        return super(SoftDeleteQuerySet, self).update(deleted_at=now())

    def hard_delete(self):
        return super(SoftDeleteQuerySet, self).delete()

    def alive(self):
        return self.filter(deleted_at=None)

    def dead(self):
        return self.exclude(deleted_at=None)

class SoftDeleteManager(models.Manager):
    def __init__(self, *args, **kwargs):
        self.alive_only = kwargs.pop('alive_only', True)
        super(SoftDeleteManager, self).__init__(*args, **kwargs)

    def get_queryset(self):
        if self.alive_only:
            return SoftDeleteQuerySet(self.model).filter(deleted_at=None)
        return SoftDeleteQuerySet(self.model)

    def hard_delete(self):
        return self.get_queryset().hard_delete()

class SoftDeleteMixin(models.Model):

    deleted_at = models.DateTimeField(blank=True, null=True, )
    objects = SoftDeleteManager()
    all_objects = SoftDeleteManager(alive_only=False)

    class Meta:
        abstract = True

    def delete(self):
        self.deleted_at = now()
        self.save()

    def hard_delete(self):
        super(SoftDeleteMixin, self).delete()