from django.utils import timezone
from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import UserManager
from base.mixins.timestamp import (
    AutoCreatedUpdatedMixin, SoftDeleteMixin,
)

class User(
    AbstractBaseUser,
    PermissionsMixin,
    AutoCreatedUpdatedMixin,
    SoftDeleteMixin
):
    # _()은 i18n 될 수 있는 함수를 의미

    class Meta:
        ordering = ('-created_at',)

    email = models.EmailField(max_length=255, unique=True, )
    username = models.CharField(max_length=30, )
    has_terms = models.BooleanField(default=False, )
    has_privacy_policy = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, )
    is_admin = models.BooleanField(default=False, )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'has_terms', 'has_privacy_policy', ]

    def __str__(self):
        return "username: " + self.username

    def get_full_name(self):        
        return self.username

    def get_short_name(self):
        return self.username

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])
        
    def save(self, *args, **kwargs):
        return super(User, self).save(*args, **kwargs)
    
    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.is_admin

