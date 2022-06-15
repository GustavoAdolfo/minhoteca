import logging
from django.core import mail
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages, auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
import environ
from .tokens import account_activation_token
from .forms import CreateUserForm, UserProfileForm
from .models import MinhotecaUser


env = environ.Env()
environ.Env.read_env()
log = logging.getLogger()
log.setLevel(logging.INFO)

def create_user(request):
    if request.method != 'POST':
        form = CreateUserForm()
        return render(request, 'account.html', {'form': form})

    form = CreateUserForm(request.POST)
    try:
        if form.is_valid():
            new_user = form.save()
            if new_user:
                current_site = get_current_site(request)
                subject = 'Confirme seu cadastro na Minhoteca'
                to_email = form.cleaned_data.get('email')
                message = render_to_string(
                    'emails/account_activation_email.html',
                    {
                        'user': new_user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(
                            force_bytes(new_user.pk)),
                        'token': account_activation_token.make_token(
                            new_user),
                    })
                plain_message=strip_tags(message)
                mail.send_mail(subject, plain_message,
                    from_email=env('DEFAULT_FROM_EMAIL'),
                    recipient_list=[to_email], html_message=message)
                # email = EmailMessage(subject, message, to=[to_email])
                # email.send()
                # new_user.email_user(subject, message)
                messages.add_message(
                    request,
                    messages.SUCCESS,
                    'Foi enviado um e-mail de confirmação com instruções para '+
                    'validar sua conta.<br/>Aguardo você em breve!')
                messages.add_message(
                    request,
                    messages.INFO,
                    'Você só poderá solicitar empréstimos após ' +
                    'completar seu perfil e ter seu cadastro aprovado.',
                    extra_tags='safe')
                return HttpResponseRedirect('/')
        
        return render(request, 'account.html', {'form': form})
    except Exception as error:
        log.error(error)
        messages.warning(
            request,
            ('Ocorreu uma falha ao realizar o cadastro. '+
            'Por favor tente novamente mais tarde.')
        )
        return render(request, 'account.html', {'form': form})



def confirmation(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = MinhotecaUser.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError): #MinhotecaUser.DoesNotExist
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed = True
        user.save()
        messages.success(
            request, (
                'E-mail confirmado com sucesso. Faça login para continuar.'))
        return HttpResponseRedirect(reverse('accounts:login'))
    else:
        log.error(['Falha em confirmação de conta.', request, uidb64])
        messages.warning(
            request, (
                'O link de confirmação é inválido, possivelmente ' +
                'porque ele já pode ter sido utilizado.'))
        return HttpResponseRedirect(reverse('accounts:create'))


def logoff(request):
    """Faz log out do usuário."""
    logout(request)
    request.session.flush()
    return HttpResponseRedirect('/')

def _get_profile_level(request):
    profile_complete = 8
    profile_weight = 0
    user = auth.get_user(request)
    profile_weight += 1 if user.first_name else 0
    profile_weight += 1 if user.contact_phone else 0
    profile_weight += 1 if user.email else 0
    profile_weight += 1 if user.zip_code else 0
    profile_weight += 1 if user.address else 0
    profile_weight += 1 if user.city else 0
    profile_weight += 1 if user.address_number else 0
    profile_weight += 1 if user.state else 0
    return (100 * profile_weight) // profile_complete

@login_required(login_url='/accounts/login/')
def profile(request):
    """Mostra o perfil do usuário."""
    profile_level = _get_profile_level(request)
    profile_form = UserProfileForm()
    context = { 'profile_level': profile_level, 'profile_form': profile_form }
    return render(request, 'profile.html', context)

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    """Salvar o perfil do usuário."""
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('accounts:profile'))
    
    profile_form = UserProfileForm(request.POST)
    try:
        if profile_form.is_valid():
            _ = profile_form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Perfil atualizado com sucesso.')
            return HttpResponseRedirect(reverse('accounts:profile'))
        else:
            messages.add_message(
                request,
                messages.ERROR,
                'Os dados informados não são válidos.')
            profile_level = _get_profile_level(request)
            context = {
                'profile_level': profile_level,
                'profile_form': profile_form
            }
            return render(request, 'profile.html', context)
    except Exception as error:
        log.error(error)
        messages.warning(
            request,
            ('Ocorreu uma falha ao atualizar os dados. '+
            'Por favor tente novamente mais tarde.')
        )
        return HttpResponseRedirect('/')