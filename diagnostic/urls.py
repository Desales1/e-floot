from django.urls import path
from .views import *

urlpatterns = [
    path('Connexion/garage/', login_garage, name='login_garage'),
    path('Connexion/garage/forget_apssword/', forgot_password, name='forgot_password'),
    path('espace/garage/', garage_page, name='garage_page'),
     path('faire/devis/<int:diagnostic_id>/', create_devis, name='create_devis'),
    path('display-recu/<int:devis_id>/', display_recu, name='display_recu'),
    path('submit/diagnostic/<int:voiture_id>/', faire_diagnostic, name='diagnostic'),
    path('get_diagnostic_details/<int:diagnostic_id>/', get_diagnostic_details, name='get_diagnostic_details'),
    # path('recu/<int:devis_id>/pdf/', download_pdf, name='download_pdf'),
    path('diagnostics/', list_diagnostics, name='list_diagnostics'),
    path('diagnostics/modifier/<int:diagnostic_id>/', modifier_diagnostic, name='modifier_diagnostic'),
    path('diagnostics/supprimer/<int:diagnostic_id>/', supprimer_diagnostic, name='supprimer_diagnostic'),
    path('devis/liste', list_devis, name='list_devis'),
    path('consulter/diagnostic/<int:diagnostic_id>/', consulter_diagnostic, name='consulter_diagnostic'),
]