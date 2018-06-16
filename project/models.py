from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin
from common.models import Contact, Media, Ability, Keyword


class Project(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )

    title = models.CharField(max_length=100, )
    description = models.TextField()
    profile_image = models.URLField(max_length=500, )
    started_at = models.DateTimeField(blank=True, )
    ends_at = models.DateTimeField(blank=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ManyToManyField(Contact)
    contacts = models.ManyToManyField(Media)
    abilities = models.ManyToManyField(Ability)
    keywords = models.ManyToManyField(Keyword)