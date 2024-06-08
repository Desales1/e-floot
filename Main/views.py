from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from diagnostic.models import Devis
from .models import envoi_contact
from admin_dashboard.models import Garage, Voiture
from django.contrib import messages
from django.core.mail import send_mail
from .permissions import superuser_required
from django.template.loader import render_to_string


# Create your views here.
def home(request,):
    garages = Garage.objects.all().order_by('-id')
    
    # formulaire d'envoi de contact
    if request.method == "POST":
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        message = request.POST.get('message')

        newContact = envoi_contact()
        newContact.nom = nom
        newContact.email = email
        newContact.message = message
        newContact.save()
        messages.success(request, 'Merci votre message ! ')
        return redirect('/')

    datas = {
        "garages":garages,
    }
    return render(request, 'index.html', datas)

def add_car(request):
    return render(request, 'user_add_car.html')


#  assigner une voiture à un garage 
@superuser_required
def assign_voiture(request, voiture_id):
    voiture = get_object_or_404(Voiture, pk=voiture_id)
    garages = Garage.objects.all()

    if request.method == 'POST':
        garage_id = request.POST.get('garage')
        try:
            garage = Garage.objects.get(pk=garage_id)
        except Garage.DoesNotExist:
            messages.error(request, "Le garage sélectionné n'existe pas.")
            return redirect('assign_voiture', voiture_id=voiture_id)
    
     # Vérifiez si la voiture est déjà assignée à ce garage
        if voiture.garage_assigne == garage:
            messages.error(request, f"La voiture {voiture.modele} est déjà assignée au garage {garage.name}.")
            return redirect('assign_voiture', voiture_id=voiture_id)

        voiture.garage_assigne = garage
        voiture.statut = 'en attente de diagnostic'
        voiture.save()

        contexts = {
            'voiture': voiture,
            'garage': garage
        }
        # Envoyer un email au garage
        subject = 'Nouvelle voiture assignée pour diagnostic'
        message = f'Une nouvelle voiture a été assignée à votre garage pour diagnostic.'
        from_email = settings.EMAIL_HOST_USER
        recipient_list = [garage.email]
        notice_html = render_to_string('emailAssign.html', contexts)
        send_mail(subject, message, from_email, recipient_list, fail_silently=False, html_message=notice_html)

        messages.success(request, f'Voiture {voiture.modele} a été assignée au garage {garage.name}.')
        return redirect('dashboard')
    
    contexts = {
        'voiture': voiture,
        'garages': garages
    }
    return render(request, 'assign_voiture.html', contexts)