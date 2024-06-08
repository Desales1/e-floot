from django.db import models
from django.conf import settings
import uuid

# Create your models here.
class type_client(models.Model):
    TYPECHOICES = (
        ('Particulier', 'Particulier'),
        ('Entreprise', 'Entreprise'),
        ('Garage', 'Garage'),
    )
    type = models.CharField(choices=TYPECHOICES, max_length=20)

    def __str__(self):
        return self.type




class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    termes_accept = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    addresse = models.CharField(max_length=255, blank=True, null=True)
    auth_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    is_verified = models.BooleanField(default=True)

    def __str__(self):
        return self.user.username
