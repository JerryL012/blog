from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm

def register(request):
    if request.method == 'POST':
        # use the new form in forms.py
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Welcome {username}! You are now able to login')
            # redirect to home page
            return redirect('login')
    else:
        # empty form
        form = UserRegisterForm()
    context = {
        'form': form
    }
    return render(request, 'users/register.html', context)
