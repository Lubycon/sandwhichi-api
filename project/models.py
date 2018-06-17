import datetime
from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin
from common.models import Contact, Media, Ability, Keyword
from user.models import User


class Schedule(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )
    
    monday = models.BooleanField(default=False, )
    tuesday = models.BooleanField(default=False, )
    wednesday = models.BooleanField(default=False, )
    thursday = models.BooleanField(default=False, )
    friday = models.BooleanField(default=False, )
    saturday = models.BooleanField(default=False, )
    sunday = models.BooleanField(default=False, )
    is_negotiable = models.BooleanField(default=False, )
    start_time = models.TimeField(default=datetime.time(00, 00), )
    end_time = models.TimeField(default=datetime.time(00, 00), )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class ScheduleRecurringType(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )
    
    name = models.CharField(max_length=20, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class DescriptionQuestion(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )

    question = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class ProjectDescription(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )

    question = models.ForeignKey(DescriptionQuestion, on_delete=models.PROTECT, )
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Project(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )

    title = models.CharField(max_length=100, )
    description = models.ForeignKey(ProjectDescription, on_delete=models.PROTECT, )
    profile_image = models.URLField(max_length=500, )
    started_at = models.DateTimeField(blank=True, )
    ends_at = models.DateTimeField(blank=True, )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    media = models.ManyToManyField(Contact)
    contacts = models.ManyToManyField(Media)
    abilities = models.ManyToManyField(Ability)
    keywords = models.ManyToManyField(Keyword)


class ProjectUserView(models.Model):
    class Meta:
        ordering = ('-created_at', )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, )
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, )