from django.shortcuts import render, redirect
from rest_framework import viewsets
from .import models 
from .import seiralizers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token

# for sending emaill 
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string


class PatientViewset(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = seiralizers.PatientSerializer


class PatientRegistraionApiview(APIView):
    serializer_class = seiralizers.RegistrationSerializer

    def post(self, request):
        seiralizer = self.serializer_class(data=request.data)

        if seiralizer.is_valid():
            user = seiralizer.save()
            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            confirm_link = f"https://creat-stream.onrender.com/patient/active/{uid}/{token}"
            email_subject = 'Confirm Your Email'
            email_body = render_to_string('confirm_email.html',{'confirm_link':confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response('Check Your Email for Confirmation')
        
        return Response(seiralizer.errors)


def activate(request, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    
    except(User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('login')
    
    else:
        return redirect('register')
    
class patientLoginApiView(APIView):
    def post(self, request):
        seiralizer = seiralizers.LogoinSerializer(data= self.request.data)

        if seiralizer.is_valid():
            username = seiralizer.validated_data['username']
            password = seiralizer.validated_data['password']

            user = authenticate(username = username, password = password)

            if user:
                token, _ = Token.objects.get_or_create(user = user)
                login(request,user)
                return Response({'token':token.key, 'user_id': user.id})
            
            else:
                return Response({'error':'Invalid Credential'})
        return Response(seiralizer.errors)
    

class PatientLogoutApiView(APIView):
    def get(self, request):
        request.user.auth_token.delete()
        logout(request)

        return Response({'success':'Logout Successfully'})