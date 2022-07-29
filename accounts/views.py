import logging
from django.core import mail
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.html import strip_tags
from django.http import HttpResponseRedirect
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages, auth
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import SetPasswordForm
import environ
import base64
from .tokens import account_activation_token
from .forms import CreateUserForm, UserProfileForm, PwdChangeForm
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
                    'validar sua conta.<br/>Aguardo você em breve!',
                    extra_tags='success safe')
                messages.add_message(
                    request,
                    messages.INFO,
                    'Você só poderá solicitar empréstimos após ' +
                    'completar seu perfil e ter seu cadastro aprovado.',
                    extra_tags='info safe')
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

def _get_profile_level(user):
    profile_complete = 8
    profile_weight = 0
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
def get_profile(request):
    """Mostra o perfil do usuário."""
    user = auth.get_user(request)
    try:
        user_profile = get_object_or_404(MinhotecaUser, id=user.id)
        profile_level = _get_profile_level(user_profile)
        profile_form = UserProfileForm(instance=user_profile)
        context = { 'profile_level': profile_level, 'profile_form': profile_form }
        return render(request, 'profile.html', context)
    except Exception as error:
        log.error(error)
        messages.warning(
            request,
            ('Ocorreu um erro ao carregar seu perfil. '+
            'Por favor tente novamente mais tarde.')
        )
        return HttpResponseRedirect('/')


def _update_profile(request, current_profile):
    profile_form = UserProfileForm(
        instance=current_profile,
        data=request.POST) #, files=request.FILES)
    if profile_form.is_valid():
        current_profile = profile_form.save(commit=False)
        current_profile.save()
        return None
    
    return profile_form

def _create_new_profile(request):
    profile_form = UserProfileForm(request.POST) #, request.FILES)
    if profile_form.is_valid():
        new_profile = profile_form.save(commit=False)
        new_profile.email = request.user.email
        # new_profile.can_borrow = \
        #     len(new_profile.first_name.strip()) > 0 and \
        #         len(new_profile.contact_phone.strip()) > 0 and \
        #             len(new_profile.last_name.strip()) > 0 and \
        #                 len(new_profile.zip_code.strip()) > 0 and \
        #                     len(new_profile.address.strip()) > 0 and \
        #                         len(new_profile.city.strip()) > 0 and \
        #                             len(new_profile.address_number.strip()) > 0 and \
        #                                 len(new_profile.state.strip()) > 0
        new_profile.save()

@login_required(login_url='/accounts/login/')
def edit_profile(request):
    """Salvar o perfil do usuário."""
    if request.method != 'POST':
        return HttpResponseRedirect(reverse('accounts:profile'))
    
    user = auth.get_user(request)
    try:
        if MinhotecaUser.objects.filter(id=user.id).exists():
            profile = get_object_or_404(MinhotecaUser, id=user.id)
            update_form = _update_profile(request, profile)
            if not update_form:
                messages.add_message(request, messages.SUCCESS,
                                        'Perfil atualizado com sucesso!')
                return HttpResponseRedirect('/')
            else:
                messages.add_message(
                    request,
                    messages.ERROR,
                    'Os dados informados não são válidos.')
                profile_form = UserProfileForm(request.POST) #, request.FILES)
                profile_level = _get_profile_level(profile)
                context = {
                    'profile_level': profile_level,
                    'profile_form': profile_form
                }
                return render(request, 'profile.html', context)
        else:
            _create_new_profile(request)
            messages.add_message(request, messages.SUCCESS,
                                    'Perfil criado com sucesso!')
            messages.add_message(request, messages.INFO, 'Em breve você ' +
            'receberá um e-mail confirmando a aprovação para emprestímo.')
            return HttpResponseRedirect('/')
    except Exception as error:
        log.error(error)
        messages.error(
            request,
            ('Ocorreu uma falha ao atualizar os dados. '+
            'Por favor tente novamente mais tarde.')
        )
        return HttpResponseRedirect('/')


@login_required(login_url='user/login/')
def changepassword(request):
    if request.method == "POST":
        form = PwdChangeForm(data=request.POST, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your Password Changed",
                             extra_tags='green')
            return redirect('crmapp')
    else:
        form = PwdChangeForm(user=request.user)
    context = {'form': form}
    return render(request, 'changepassword.html', context)


def reset_password_confirm(request, uidb64, token,
                           token_generator=default_token_generator):
    """
    View that checks the hash in a password reset link and presents a
    form for entering a new password.
    """
    assert uidb64 is not None and token is not None  # checked by URLconf

    try:
        uidb64 += "=" * ((4 - len(uidb64) % 4) % 4)
        uid_int = int(base64.b64decode(uidb64))
        user = MinhotecaUser.objects.get(id=uid_int)
    except Exception as e:
        print(e)
        user = None

    ctx = {}

    if user is not None and token_generator.check_token(user, token):
        ctx['validlink'] = True
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect(reverse('accounts:reset_password_complete'))
            else:
                ctx['form'] = form
                return render(request, 'reset_password_confirm.html', ctx)
        else:
            form = SetPasswordForm(user, request.GET)
            ctx['form'] = form
            return render(request, 'reset_password_confirm.html', ctx)
    else:
        ctx['validlink'] = False
        messages.add_message(
            request, messages.ERROR, 'Este link não é mais válido. Se deseja alterar sua senha, solicite novamente.')
        return HttpResponseRedirect(reverse('accounts:reset_password'))


class ChangePasswordView(View):

    def get(self, request, *args, **kwargs):
        user = request.user
        context = {'user': user}
        return render(request, 'change_password.html', context)

    def post(self, request, *args, **kwargs):
        try:
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(
                    request, "Você precisa fazer login novamente para validar a nova senha.")
                return HttpResponseRedirect(reverse('accounts:logout'))
            else:
                ctx = {}
                ctx['form'] = form
                return render(request, 'change_password.html', ctx)
        except Exception as error:
            log.error(error)
            messages.error(
                request,
                ('Ocorreu uma falha ao atualizar os dados. '+
                'Por favor tente novamente mais tarde.')
            )
            return HttpResponseRedirect(reverse('accounts:change_password'))