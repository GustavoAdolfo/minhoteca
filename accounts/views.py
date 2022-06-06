from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_text

from .tokens import account_activation_token
from .forms import CreateUserForm


def create_user(request):
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            try:
                new_user = form.save()
                if new_user:
                    messages.add_message(
                        request,
                        messages.WARNING,
                        'Você só poderá solicitar empréstimos após completar ' +
                        'seu perfil e ter seu cadastro aprovado.')

                    current_site = get_current_site(request)
                    subject = 'Activate Your MySite Account'
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
                    new_user.email_user(subject, message)
                    messages.success(
                        request,
                        ('Enviamos um e-mail para que você confirme sua conta.')
                    )
                    return HttpResponseRedirect('accounts/confirmation/')
            except Exception as e:
                print(e)  # TODO: Log error; Message... etc
                return render(request, 'account.html', {'form': form})
    else:
        form = CreateUserForm()
    return render(request, 'account.html', {'form': form})


def confirmation(request):
    return render(request, 'confirmation.html')
