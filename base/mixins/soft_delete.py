# -*- coding: UTF-8 -*-

from django.db import models
from django.utils.timezone import now

class SoftDeleteMixin(models.Model):

    deleted_at = models.DateTimeField(blank=True, null=True, )

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        self.deleted_at = now()
        self.updated
        kwargs = {
            'using': using,
        }
        if hasattr(self, 'updated_at'):
            kwargs['disable_auto_updated_at'] = True
        self.save(**kwargs)