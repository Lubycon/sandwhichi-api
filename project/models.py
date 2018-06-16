from django.db import models
from base.mixins.timestamp import (
    AutoCreatedUpdatedMixin, SoftDeleteMixin,
)

class Project(AutoCreatedUpdatedMixin, SoftDeleteMixin):
    class Meta:
        ordering = ('-created_at', )

    title = models.CharField(max_length=100, )
    description = models.TextField()
    profile_image = models.URLField(max_length=500, )
    started_at = models.DateTimeField(blank=True, )
    ends_at = models.DateTimeField(blank=True, )