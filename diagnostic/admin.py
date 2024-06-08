from django.contrib import admin
from .models import *

class DevisFieldInline(admin.TabularInline):
    model = DevisField
    extra = 1  # Nombre de champs supplémentaires vierges à afficher

class DevisAdmin(admin.ModelAdmin):
    inlines = [DevisFieldInline]
    list_display = ('title',)  # Afficher le titre du devis dans la liste des devis

# Enregistrement des modèles avec les classes d'administration personnalisées
admin.site.register(Devis, DevisAdmin)
admin.site.register(Diagnostic)
admin.site.register(DevisField) 
