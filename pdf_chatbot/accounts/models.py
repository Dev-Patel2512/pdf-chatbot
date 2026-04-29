from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


phone_validator = RegexValidator(
    regex=r'^\+?1?\d{9,15}$',
    message="Phone number must be entered in format: '+999999999'. Up to 15 digits allowed."
)


class CustomUser(AbstractUser):
    phone_number = models.CharField(
        validators=[phone_validator],
        max_length=17,
        unique=True,
        help_text='Required. Enter a valid phone number.'
    )
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    REQUIRED_FIELDS = ['phone_number', 'email']

    def __str__(self):
        return self.username

    def get_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[:2].upper()
