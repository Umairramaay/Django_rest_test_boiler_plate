from django.urls import path, include
from rest_framework import routers
from patients.views import PatientViewSet, AppointmentDetailUpdateDestroyView,AppointmenListFilterView, \
                            AppointmentListCreateView


router = routers.DefaultRouter()
router.register(r'pets', PatientViewSet, basename='patients')

urlpatterns = [
    path('', include(router.urls)),
    path("appointment_create/", AppointmentListCreateView.as_view(),name='appointment-list-create'),
    path("appointment/<pk>/", AppointmentDetailUpdateDestroyView.as_view(),name='appointment'),
    path("appointment_filters/", AppointmenListFilterView.as_view(),name='appointment-filters'),
]