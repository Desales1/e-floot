from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin


# Si vous avez un formulaire personnalisé pour la création/modification de l'utilisateur, vous pouvez l'importer et l'utiliser ici.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role',)}),  # Ajoutez ici les champs personnalisés
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('role',)}),  # Ajoutez ici les champs personnalisés pour le formulaire d'ajout
    )
# Register your models here.
admin.site.register(envoi_contact)
