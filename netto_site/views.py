####################################################################################
### Anggi Agista
### email : agista.mailrespon@gmail.com
#####################################################################################
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


@login_required
def home(request):
    return render(request, 'netto/index.html')