from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
# Create your views here.




def home_view(request:HttpRequest):
    return render(request, 'main/index.html')

def error_view(request:HttpRequest):
    return render(request, 'main/error_page.html')

