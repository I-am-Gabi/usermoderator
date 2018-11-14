from django.shortcuts import render
from django.contrib.auth.decorators import login_required 

from .forms import UserForm

def register(request): 
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.set_password(user.password)
            user.status = 0
            user.save()
            form = UserForm()
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, 'account/user_form.html', {'form': form})