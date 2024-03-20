from django.shortcuts import render
from rest_framework import viewsets,filters,pagination
from .import serializers 
from .models import Doctor,Specialization,Designation,AvailableTime,Review
from rest_framework.permissions import IsAuthenticated,IsAuthenticatedOrReadOnly
# Create your views here.

class DoctorPagination(pagination.PageNumberPagination):
    page_size = 1
    page_size_query_param = page_size
    max_page_size = 50


class DoctorViewset(viewsets.ModelViewSet):
    queryset = Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer

    filter_backends = [filters.SearchFilter]
    # pagination_class = DoctorPagination
    search_fields = ['user__first_name','user__email','designation__name','specialization__name']

class SpecializationViewset(viewsets.ModelViewSet):
    queryset = Specialization.objects.all()
    serializer_class = serializers.SpecializationSerializer

class DesignationViewset(viewsets.ModelViewSet):
    queryset = Designation.objects.all()
    serializer_class = serializers.DesignationSerializer

class AvailabeTimeForSpecificDoctor(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset,view):
        doctor_id = request.query_params.get('doctor_id')

        if doctor_id:
            return queryset.filter(doctor = doctor_id)

class AvailableTimeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = AvailableTime.objects.all()
    serializer_class = serializers.AvailableTime
    filter_backends = [AvailabeTimeForSpecificDoctor]

class ReviewViewset(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = serializers.ReviewSerializer