from django.shortcuts import render
from django.http import HttpRequest ,HttpResponse
# Create your views here.

def create_event_view(request:HttpRequest):
    return render(request, 'create_event.html')




