from django.shortcuts import render

from accounts.forms import CreateUserForm


def index(request):
    form = CreateUserForm()
    return render(request, 'index.html', {'form': form})
