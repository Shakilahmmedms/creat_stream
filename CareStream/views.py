from django.contrib.auth.models import User
from rest_framework import viewsets
from .import seriailzers

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = seriailzers.UserSerializer