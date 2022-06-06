from django import forms
from django.forms.models import ModelForm
from .models import User


class CreateUserForm(ModelForm):
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Senha', widget=forms.PasswordInput,
                               max_length=30)
    confirm_password = forms.CharField(
        label='Confirmação de Senha', widget=forms.PasswordInput,
        max_length=30)
    user_term_accept = forms.BooleanField(
        required=True, label='Li e aceito os termos de uso')

    class Meta:
        model = User
        fields = ['email', 'password', 'confirm_password']

    def save(self, commit=True):
        if not self.cleaned_data['user_term_accept']:
            raise forms.ValidationError(
                'Você precia ler e aceitar os termos de uso para continuar.')

        user = User.objects.create(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']).save(commit=False)
        if commit:
            user.save()
        return user
