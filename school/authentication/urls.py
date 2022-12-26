from django.urls import path
from .views import registration_user
from .views import mail_accept
from .views import CustomLoginView
from .views import mail_sent
from .views import mail_done
from django.contrib.auth import views as s_views

urlpatterns = [
    path('register/', registration_user, name='registration'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', mail_accept, name='activate'),
    path('register/mail_accept/', mail_accept, name='mail_accept'),
    path('register/mail_sent/', mail_sent, name='mail_sent'),
    path('register/done/', mail_done, name='mail_done'),

    path('reset_password/', s_views.PasswordResetView.as_view(template_name='authentication/recovery/recovery.html'), name='reset_password'),
    path('reset_password/sent/', s_views.PasswordResetDoneView.as_view(template_name='authentication/recovery/recovery_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', s_views.PasswordResetConfirmView.as_view(template_name='authentication/recovery/password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset_password/complete/', s_views.PasswordResetCompleteView.as_view(template_name='authentication/recovery/reset_done.html'), name='password_reset_complete'),

    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', s_views.LogoutView.as_view(), name='logout'),


]