from django.shortcuts import render
from .import serializers
from .models import Service
from rest_framework import viewsets

# Create your views here.


class ServiceViewset(viewsets.ModelViewSet):
    queryset = Service.objects.all()
    serializer_class = serializers.ServiceSerializer