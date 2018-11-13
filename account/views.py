from django.shortcuts import render
from .forms import UserForm

def user_new(request): 
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  
            user.status = 0
            user.save()
            return render(request, 'account/user_form.html', {'form': form})
    else:
        form = UserForm()
    return render(request, 'account/user_form.html', {'form': form})