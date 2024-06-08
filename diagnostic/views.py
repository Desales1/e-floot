from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, update_session_auth_hash
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from Main.models import User
from .models import Devis, DevisField, Diagnostic
from admin_dashboard.models import Garage, Voiture
from authenticate.models import type_client
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from Main.permissions import garage_required
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings 
from .forms import DiagnosticForm


def login_garage(request):
    first_login = False
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_new_password = request.POST.get('confirm_new_password')

        if not current_password:  # Première connexion
            first_login = True
            if new_password and confirm_new_password:
                if new_password != confirm_new_password:
                    messages.error(request, 'Les mots de passe ne correspondent pas.')
                else:
                    try:
                        user = User.objects.get(email=email)
                        user.set_password(new_password)
                        user.save()
                        update_session_auth_hash(request, user)  # Mise à jour de la session
                        messages.success(request, 'Mot de passe mis à jour avec succès! Veuillez vous connecter.')
                        return redirect('login_garage')  
                    except User.DoesNotExist:
                        messages.error(request, 'Adresse e-mail invalide.')
            else:
                messages.error(request, 'Veuillez entrer et confirmer le nouveau mot de passe.')
        else:  # Connexion normale
            user = authenticate(request, username=username, password=current_password)
            if user is not None:
                login(request, user)
                return redirect('garage_page')
            else:
                messages.error(request, 'Adresse e-mail ou mot de passe invalide.')

    return render(request, 'login-garage.html', {'first_login': first_login})


#  uniquement pour les garages
def forgot_password(request):
    if request.method == 'POST':
        email = request.POST.get('forgotEmail')
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur trouvé avec cette adresse e-mail.")
            return redirect('login_garage')  # Modifier pour rediriger vers la page de connexion

        # Générer le token de réinitialisation de mot de passe
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # Créer le lien de réinitialisation de mot de passe
        reset_link = request.build_absolute_uri(reverse('reset_password')) + f'?uid={uid}&token={token}'

        # Envoyer l'e-mail de réinitialisation de mot de passe
        subject = 'Réinitialisation de mot de passe'
        message = render_to_string('email/forgot_password_email.html', {'reset_link': reset_link})
        send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email])

        messages.success(request, "Un e-mail de réinitialisation de mot de passe a été envoyé à votre adresse.")
        return redirect('login_garage')  # Modifier pour rediriger vers la page de connexion

    return render(request, 'login-garage.html')


@garage_required
def garage_page(request):
    user = request.user
     # Vérifiez que l'utilisateur est authentifié et qu'il a le rôle 'garage'
    if not user.is_authenticated or user.role != 'garage':
        messages.error(request, "Vous n'avez pas l'autorisation d'accéder à cette page.")
        return redirect('/')  

    try:
        garage = Garage.objects.get(email=user.email)
    except Garage.DoesNotExist:
        messages.error(request, "Aucun garage associé à cet utilisateur.")
        return redirect('/')  
    garage = Garage.objects.get(email=user.email)
    voitures = Voiture.objects.filter(garage_assigne=garage, statut='en attente de diagnostic')

    # Filtrer les diagnostics en fonction des voitures assignées au garage
    diagnostics = Diagnostic.objects.filter(vehicule__in=voitures)


    contexts = {
        # 'devis':devis,
        'type_client': type_client,
        'voitures': voitures,
        'garage': garage,
        'diagnostics':diagnostics,
        
    }
    return render(request, 'garage_page.html', contexts)




def create_devis(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        commentaire = request.POST.get('commentaire')
        diagnostic_id = request.POST.get('diagnostic')
        
        # Récupérer l'instance unique de Diagnostic
        diagnostic = get_object_or_404(Diagnostic, pk=diagnostic_id, garage=request.user.garage)
        
        
        devis = Devis(title=title, diagnostic=diagnostic, commentaire=commentaire)
        devis.save()

        labels = request.POST.getlist('field_label')
        types = request.POST.getlist('field_type')
        values = request.POST.getlist('field_value')
        prixs = request.POST.getlist('field_prix')

        total_prix = 0

        for label, field_type, value, prix in zip(labels, types, values, prixs):
            prix_value = float(prix) if prix else 0.0
            DevisField.objects.create(devis=devis, label=label, field_type=field_type, value=value, prix=prix_value)
            total_prix += prix_value

        devis.total_prix = total_prix
        devis.save()

        return redirect('list_devis')  # Rediriger vers la liste des devis après la création

    diagnostics = Diagnostic.objects.filter(garage=request.user.garage)
    return render(request, 'create_devis.html', {'diagnostics': diagnostics})





def get_diagnostic_details(request, diagnostic_id):
    diagnostic = Diagnostic.objects.get(id=diagnostic_id)
    data = {
        'garage_name': diagnostic.garage.name,
        'garage_email': diagnostic.garage.email,
        'garage_address': diagnostic.garage.adresse,
        'garage_telephone': diagnostic.garage.telephone,
        'garage_business_number': diagnostic.garage.telephone,
        'garage_logo': diagnostic.garage.logo_garage.url,
        'date_diagnostic': diagnostic.date_add,
    }
    return JsonResponse(data)



def faire_diagnostic(request, voiture_id):
    voiture = get_object_or_404(Voiture, id=voiture_id)
    try:
        garage = voiture.garage_assigne
    except Garage.DoesNotExist:
        messages.error(request, 'Garage not found')
        return redirect('dashboard')

    if request.method == 'POST':
        solutions = request.POST.get('solutions')
        problems = request.POST.get('problems')
        duree_diagnostic = request.POST.get('duree_diagnostic')
        method_diagnostic = request.POST.get('method_diagnostic')

        newDiagnostic = Diagnostic(
            garage=garage,
            vehicule=voiture,
            solutions=solutions,
            problems=problems,
            duree_diagnostic=duree_diagnostic,
            method_diagnostic=method_diagnostic,
        )
        newDiagnostic.save()

        voiture.statut = 'diagnostiquee'
        voiture.save()

        messages.success(request, 'Le diagnostic a été soumis avec succès.')
        return redirect('list_diagnostics')

    context = {
        'voiture': voiture,
    }
    return render(request, 'diagnostic.html', context)



def display_recu(request, devis_id):
    devis = get_object_or_404(Devis, id=devis_id)
    devis_fields = DevisField.objects.filter(devis=devis)
    context = {
        'devis': devis,
        'devis_fields': devis_fields,
    }
    return render(request, 'display_recu.html', context)


def list_diagnostics(request):
    diagnostics = Diagnostic.objects.select_related('garage', 'vehicule').all().order_by('-date_add')
    context = {
        'diagnostics': diagnostics,
        
    }
    return render(request, 'list_diagnostics.html', context)

def supprimer_diagnostic(request, diagnostic_id):
    diagnostic = get_object_or_404(Diagnostic, pk=diagnostic_id)
    if request.method == 'POST':
        diagnostic.delete()
        return redirect('list_diagnostics')
    return redirect('list_diagnostics')  


def modifier_diagnostic(request, diagnostic_id):
    diagnostic = get_object_or_404(Diagnostic, id=diagnostic_id)
    if request.method == 'POST':
        form = DiagnosticForm(request.POST, instance=diagnostic)
        if form.is_valid():
            form.save()
            return redirect('list_diagnostics')  # Rediriger vers la liste des diagnostics après modification
    else:
        form = DiagnosticForm(instance=diagnostic)
    return render(request, 'modifier_diagnostic.html', {'form': form})

def list_devis(request):
    devis = Devis.objects.all()
    return render(request, 'list_devis.html', {'devis': devis})

