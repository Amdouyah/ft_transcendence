from django.shortcuts import render

# from django.http import HttpResponse
from .models import Message
from django.views import View
from django.http import HttpRequest
from django.http import JsonResponse
import json

class Begin(View):
    def get(self, request: HttpRequest):
        return render(request, 'chat/test.html')

    def post(self, request):
        return render(request, 'chat/test.html')

# Create your views here.
#contains the business logic, processes the requests,  and  return respons 
 