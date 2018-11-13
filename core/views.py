from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
 
@csrf_protect
@login_required
def index(request):
    return render(request, 'core/index.html')

