from django.urls import path 
from .views import *
from django.contrib.auth import views as auth_views




urlpatterns = [
    # URLs pour connexion et inscription et deconnexion
    path('signout', signout, name='signout'),
    path('connexion/', connexion, name='connexion'),
    path(f'connexion/en-tant-que/', login_user, name='login'),
    path('creationCompte/pour-un/', register, name='registerP'),

    # URLs pour email verification
    path('token' , token_send , name="token_send"),
    path('verify/<str:auth_token>/', verify, name='verify'),
    path('error/', error_page, name='error_page'),
    path('success' , success , name='success'),
    path('confirm-email/<str:token>/', confirm_email, name='confirm_email'),
   

    # URLs password reset
    path('password_reset/', password_reset_request, name='password_reset'),
    path('password_reset_done/<str:type_client>/', password_reset_done, name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/<str:type_client>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset-complete/<str:type_client>/',
         auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),
         name='password_reset_complete')
     
]