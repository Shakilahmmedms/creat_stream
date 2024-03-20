from rest_framework.routers import DefaultRouter
from django.urls import path,include
from .import views

router = DefaultRouter()

router.register('list',views.PatientViewset)

urlpatterns = [
    path('', include(router.urls)),
    path('register/',views.PatientRegistraionApiview.as_view(), name='register'),
    path('login/',views.patientLoginApiView.as_view(), name='login'),
    path('logout/',views.PatientLogoutApiView.as_view(), name='logout'),
    path('active/<uid64>/<token>/',views.activate, name='activate'),
]
