from django.contrib.auth.views import LoginView
from django.shortcuts import render
import random

from django.contrib.auth import get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect, HttpResponse
from django.template.loader import render_to_string
from django.urls import reverse
from django.contrib import messages

from .forms import SignUpFrom, ProfileForm

from .token import account_activation_token
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str

"""Функция регистрации пользователя"""


def registration_user(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = SignUpFrom(request.POST)
            profile = ProfileForm(request.POST)
            if request.POST.get('password1') != request.POST.get('password2'):
                messages.error(request, 'Failed PASSWORD')
                return HttpResponseRedirect(reverse('registration'))  # Если пароли не совпадают
            if form.is_valid() and profile.is_valid():
                user = form.save()
                user.is_active = False
                form.save()
                current_site = get_current_site(request)
                mail_subject = 'Activation link has been sent to your email id'
                message = render_to_string('authentication/confirm_email.html', {  # TODO: сделать шаблон письма
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                to_email = form.cleaned_data.get('email')
                email = EmailMessage(mail_subject, message, to=[to_email])
                email.send()

                user.profile.university = profile.cleaned_data.get('university')
                user.profile.phone = profile.cleaned_data.get('phone')
                user.profile.first_name = profile.cleaned_data.get('first_name')
                user.profile.last_name = profile.cleaned_data.get('last_name')
                user.profile.patronymic_name = profile.cleaned_data.get('patronymic_name')
                user.profile.university_faculty = profile.cleaned_data.get('university_faculty')
                user.profile.university_specitality = profile.cleaned_data.get('university_specitality')
                user.profile.university_course = profile.cleaned_data.get('university_course')
                user.profile.school_program = profile.cleaned_data.get('school_program')
                user.profile.save()

                username = form.cleaned_data.get('username')
                messages.success(request, f'Создан аккаунт {username}!')
                return redirect('registration')  # TODO: уведомление об отправке письма,
        else:
            form = SignUpFrom()
            profile = ProfileForm()

        context = {
            "form": form,
            'profile': profile

        }
        return render(request, 'authentication/registration/registration.html', context)
    else:
        return redirect('home')


"""Функция активации акканута пользователя"""


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you!')
    else:
        return HttpResponse('INVALID!')


"""Вход в аккаунт"""


class CustomLoginView(LoginView):
    template_name = 'authentication/login/login.html'
    redirect_authenticated_user = 'home'
