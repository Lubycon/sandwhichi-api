import datetime
from django.db import models
from base.mixins.soft_delete import SoftDeleteMixin
from common.models import (
    Contact, Media, Ability, Keyword
)
from location.models import Location
from user.models import User


class ScheduleRecurringType(SoftDeleteMixin, models.Model):
    name = models.CharField(max_length=20, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Schedule(SoftDeleteMixin, models.Model):
    monday = models.BooleanField(default=False, )
    tuesday = models.BooleanField(default=False, )
    wednesday = models.BooleanField(default=False, )
    thursday = models.BooleanField(default=False, )
    friday = models.BooleanField(default=False, )
    saturday = models.BooleanField(default=False, )
    sunday = models.BooleanField(default=False, )
    is_negotiable = models.BooleanField(default=False, )
    recurring_type = models.ForeignKey(ScheduleRecurringType, on_delete=models.PROTECT, default=1, )
    start_time = models.TimeField(default=datetime.time(00, 00), )
    end_time = models.TimeField(default=datetime.time(00, 00), )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class DescriptionQuestion(SoftDeleteMixin, models.Model):
    question = models.CharField(max_length=255, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class Project(SoftDeleteMixin, models.Model):
    class Meta:
        ordering = ('-created_at', )

    title = models.CharField(max_length=100, )
    profile_image = models.URLField(max_length=500, )
    started_at = models.DateField(blank=True, )
    ends_at = models.DateField(blank=True, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
    media = models.ManyToManyField(Media)
    contacts = models.ManyToManyField(Contact)
    abilities = models.ManyToManyField(Ability)
    keywords = models.ManyToManyField(Keyword)
    schedule = models.OneToOneField(Schedule, on_delete=models.PROTECT, )
    location = models.ForeignKey(Location, on_delete=models.PROTECT, )


class ProjectUserView(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, )
    project = models.ForeignKey(Project, on_delete=models.CASCADE, )
    created_at = models.DateTimeField(auto_now_add=True, )


class ProjectDescription(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, )
    question = models.ForeignKey(DescriptionQuestion, on_delete=models.PROTECT, )
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )


class ProjectMember(models.Model):
    project = models.ForeignKey(Project, on_delete=models.PROTECT, )
    user = models.ForeignKey(User, on_delete=models.CASCADE, )
    role = models.CharField(max_length=20, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )
