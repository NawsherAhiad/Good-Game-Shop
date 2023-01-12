from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Log

# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! you can login now')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required    
def profile(request):
    superuser = User.objects.get(is_superuser=True)
    logs = Log.objects.all()
    sum=0
    for log in logs:
        sum+=log.amount
        
    return render(request, 'users/profile.html', {'point':superuser.profile.point, 'earnings':sum})