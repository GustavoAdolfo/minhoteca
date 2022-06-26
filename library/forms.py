from datetime import datetime, timedelta
from multiprocessing.sharedctypes import Value
from sched import scheduler
from django import forms
from django.forms.models import ModelForm
from django.contrib.auth import get_user_model
from .models import Borrowing, Book


def _get_saturdays():
    """Retorna lista de sábados."""
    saturday_list = []
    today = datetime.now()
    weekday = today.weekday()
    new_day = None
    if weekday == 5:
        new_day = today + timedelta(days=7)
    elif weekday == 6:
        new_day = today + timedelta(days=6)
    else:
        new_day = today + timedelta(days=(5 - weekday))

    if new_day:
        saturday_list.append((new_day.strftime('%d/%m/%Y'), new_day.date()))
        new_day = saturday_list[0][1] + timedelta(days=7)
        saturday_list.append((new_day.strftime('%d/%m/%Y'), new_day))

    return saturday_list

class BorrowingForm(ModelForm):
    saturdays = _get_saturdays()
    date_borrowed = forms.ChoiceField(
            choices=saturdays,
            label='Escolha uma data',
            label_suffix = ": ",
            required = True,
            disabled = False,
            widget=forms.Select(
                attrs={
                    'class': 'form-select',
                    'aria-label': 'Selecione uma data'
                    }))
    borrower_id = forms.CharField(widget=forms.HiddenInput)
    book_id = forms.CharField(widget=forms.HiddenInput)
    schedule = forms.ChoiceField(
            choices=[
                ('08:00', datetime(2022,1,1,8,0).time()),
                ('09:00', datetime(2022,1,1,9,0).time()),
                ('14:00', datetime(2022,1,1,14,0).time()),
                ('15:00', datetime(2022,1,1,15,0).time()),
                ('16:00', datetime(2022,1,1,16,0).time())
                ],
            label='Escolha um horário',
            label_suffix = ": ",
            required = True,
            disabled = False,
            widget=forms.RadioSelect(
                attrs={'class': 'form-check-input mx-2'}
            )
    )

    class Meta:
        model = Borrowing
        fields = ['book_id', 'date_borrowed', 'borrower_id', 'schedule']

    def clean(self):
        cleaned_data = super().clean()
        date_borrowed = cleaned_data.get('date_borrowed')
        date_returned = cleaned_data.get('date_returned')
        if date_borrowed > date_returned:
            raise forms.ValidationError(
                'Date borrowed must be before date returned')
            
    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.date_borrowed = self.cleaned_data.get('date_borrowed')
        instance.borrower = get_user_model().objects.get(
            id=self.cleaned_data.get('borrower_id'))
        instance.book = Book.objects.get(id=self.cleaned_data.get('book_id'))
        instance.schedule = self.cleaned_data.get('schedule')
        if commit:
            instance.save()

        return instance
