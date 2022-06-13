from django import forms
from django.contrib.auth.forms import PasswordChangeForm as PdwChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import MinhotecaUser as MinhotecaUser
# from captcha.fields import CaptchaField


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    # password = forms.CharField(label='Senha', widget=forms.PasswordInput,
    #                            max_length=30)
    # confirm_password = forms.CharField(
    #     label='Confirmação de Senha', widget=forms.PasswordInput,
    #     max_length=30)
    user_term_accept = forms.BooleanField(
        required=True, label='Li e aceito os termos de uso')

    class Meta:
        model = MinhotecaUser
        fields = ['email','user_term_accept']

    def save(self, commit=True):
        if not self.cleaned_data['user_term_accept']:
            raise forms.ValidationError(
                'Você precia ler e aceitar os termos de uso para continuar.')

        user = get_user_model().objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user
