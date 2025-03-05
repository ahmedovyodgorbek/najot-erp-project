from datetime import timedelta

from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, RegexValidator
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken

from app_groups.models import GroupModel


class CustomUserModel(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    image = models.ImageField(upload_to='profile/images/',
                              null=True,
                              blank=True,
                              validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png', 'jpeg'])])
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Enter a valid phone number.")
    phone_number = models.CharField(validators=[phone_regex], max_length=15, blank=True, null=True)

    group = models.ForeignKey(
        GroupModel,
        models.SET_NULL,
        null=True,
        blank=True,
        related_name='members'
    )
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='student')

    GENDER_CHOICES = (
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    )
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.role})"

    def get_tokens(self):
        refresh = RefreshToken.for_user(self)
        refresh.set_exp(lifetime=timedelta(days=7))
        refresh.access_token.set_exp(lifetime=timedelta(days=1))

        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
