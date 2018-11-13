from django.shortcuts import render 
from .forms import InstituteForm

def institute_new(request): 
    if request.method == "POST":
        form = InstituteForm(request.POST)
        if form.is_valid():
            institute = form.save(commit=False)   
            institute.save()
            return render(request, 'institutes/institute_form.html', {'form': form})
    else:
        form = InstituteForm()
    return render(request, 'institutes/institute_form.html', {'form': form}) 
