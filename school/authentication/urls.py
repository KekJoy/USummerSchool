from django.urls import path
from .views import registration_user
from .views import activate
from .views import CustomLoginView
from django.contrib.auth import views
urlpatterns = [
    path('register/', registration_user, name='registration'),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/',
    activate, name='activate'),
    path('login/', CustomLoginView.as_view(), name='login'),

]