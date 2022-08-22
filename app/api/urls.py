from django.urls import include, path
from rest_framework import routers

from .views import PatientViewSet, PatientViewSetTwo

router = routers.DefaultRouter()
router.register(r'patient', PatientViewSet)
router.register(r'test', PatientViewSetTwo)

urlpatterns = [
    path('', include(router.urls))
]
