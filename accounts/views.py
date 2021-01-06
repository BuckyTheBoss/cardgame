from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

from django.shortcuts import render, redirect

# Create your views here.


def signup_view(request):
    form = UserCreationForm(request.POST)
    if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('show_deck')
    return render(request, 'registration/signup.html', {'form': form})

