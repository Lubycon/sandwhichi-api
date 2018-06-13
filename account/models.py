from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin
)
from .managers import UserManager

class User(AbstractBaseUser):
    # _()은 i18n 될 수 있는 함수를 의미

    class Meta:
        ordering = ('-created_at',)

    email = models.EmailField(max_length=255, unique=True, )
    username = models.CharField(max_length=30, )
    has_terms = models.BooleanField(default=False, )
    has_privacy_policy = models.BooleanField(default=False, )
    is_active = models.BooleanField(default=True, )
    is_admin = models.BooleanField(default=False, )
    created_at = models.DateTimeField(default=timezone.now, )

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'has_terms', 'has_privacy_policy', ]

    def get_full_name(self):        
        return self.username

    def get_short_name(self):
        return self.username
    
    @property
    def is_staff(self):
        return self.is_admin

