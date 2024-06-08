from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class User(AbstractUser):
    ROLE_NORMAL = 'normal'
    ROLE_GARAGE = 'garage'
    ROLE_CHOICES = [
        (ROLE_NORMAL, 'Normal'),
        (ROLE_GARAGE, 'Garage'),
    ]
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default=ROLE_NORMAL,
    )
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set', 
        blank=True,
        help_text=_(
            'The groups this user belongs to. A user will get all permissions '
            'granted to each of their groups.'
        ),
        verbose_name=_('groups'),
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',  # Change related_name to avoid conflict
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('user permissions'),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username



# Create your models here.
class envoi_contact(models.Model):
    nom = models.CharField(max_length=12)
    email = models.EmailField()
    message = models.TextField()

    # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self) :
        return f"Message de {self.nom}"