from django.db import models
from admin_dashboard.models import Garage, Voiture


class Diagnostic(models.Model):
    garage = models.ForeignKey(Garage, on_delete=models.CASCADE)
    vehicule = models.ForeignKey(Voiture, on_delete=models.CASCADE)
    solutions = models.TextField()
    problems = models.TextField()
    duree_diagnostic = models.IntegerField()
    method_diagnostic = models.TextField()

     # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__ (self):
        return f'Diagnostic du {self.garage.name} du {self.date_add} sur le vehicule {self.vehicule.numero_serie}'


# 
class Devis(models.Model):
    title = models.CharField(max_length=255)
    diagnostic = models.ForeignKey(Diagnostic, on_delete=models.CASCADE)
    commentaire = models.TextField()
    total_prix = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.title} sur le diagnostic du {self.diagnostic.date_add} du garage {self.diagnostic.garage.name}'


# 
class DevisField(models.Model):
    devis = models.ForeignKey(Devis, on_delete=models.CASCADE)
    label = models.CharField(max_length=255)  # Libellé du champ
    field_type = models.CharField(max_length=20)  # Type de champ (text, number, date, etc.)
    value = models.TextField()  # Valeur du champ

     # standards
    date_add = models.DateTimeField(auto_now_add=True)
    date_update = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.label
    
