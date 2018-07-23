from django.db import models
from django.core.mail import send_mail
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import UserManager
from base.mixins.soft_delete import SoftDeleteMixin

class User(AbstractBaseUser, PermissionsMixin, SoftDeleteMixin):
    # _()은 i18n 될 수 있는 함수를 의미

    class Meta:
        ordering = ('-created_at', )

    email = models.EmailField(max_length=255, unique=True, )
    username = models.CharField(max_length=30, )
    has_terms = models.BooleanField(default=False, )
    has_privacy_policy = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, )
    is_admin = models.BooleanField(default=False, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'has_terms', 'has_privacy_policy', ]

    def __str__(self):
        return '<User %s> [email: %s] [username: %s]' % (self.pk, self.email, self.username)

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


class UserProfile(SoftDeleteMixin, models.Model):
    user = models.OneToOneField(User, related_name='profile', on_delete=models.CASCADE, primary_key=True, )
    created_at = models.DateTimeField(auto_now_add=True, )
    updated_at = models.DateTimeField(auto_now=True, )