from django import forms
from django.contrib.auth.forms import PasswordChangeForm as PdwChangeForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth import get_user_model
from .models import MinhotecaUser as MinhotecaUser
# from captcha.fields import CaptchaField


class CreateUserForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    user_term_accept = forms.BooleanField(
        required=True, label='Li e aceito os termos de uso')

    def save(self, commit=True):
        if not self.cleaned_data['user_term_accept']:
            raise forms.ValidationError(
                'Você precia ler e aceitar os termos de uso para continuar.')

        user = get_user_model().objects.create_user(
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password1']
        )
        return user

    class Meta:
        model = MinhotecaUser
        fields = ['email','user_term_accept']

class UserProfileForm(forms.ModelForm):
    first_name = forms.CharField(label='Nome', max_length=50)
    last_name = forms.CharField(label='Sobrenome', max_length=50)
    contact_phone = forms.CharField(label='Telefone', max_length=11)
    zip_code = forms.CharField(label='CEP', max_length=8)
    address = forms.CharField(label='Endereço', max_length=100)
    address_number = forms.CharField(label='Número', max_length=10)
    address_complement = forms.CharField(label='Complemento', max_length=50)
    neighborhood = forms.CharField(label='Bairro', max_length=50)
    city = forms.CharField(label='Cidade', max_length=50)
    state = forms.CharField(label='Estado', max_length=2)

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.contact_phone = self.cleaned_data['contact_phone']
        user.zip_code = self.cleaned_data['zip_code']
        user.address = self.cleaned_data['address']
        user.address_number = self.cleaned_data['address_number']
        user.address_complement = self.cleaned_data['address_complement']
        user.can_borrow = user.first_name and user.contact_phone and \
            user.email and user.zip_code and user.address and user.city and \
                user.address_number and user.state
        if commit:
            user.save()
        
        return user        

    class Meta:
        model = MinhotecaUser
        fields = ['first_name', 'last_name', 'contact_phone', 'zip_code',
            'address', 'address_number', 'address_complement',
            'neighborhood', 'city', 'state']