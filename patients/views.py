from rest_framework import viewsets, generics
from rest_framework.response import Response
from patients.models import Patient,Appointment
from patients.serializers import PatientSerializer,ApointmentSerializer
from patients.filters import get_filtered_data

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    

class AppointmenListFilterView(generics.ListAPIView):
    
    def get_queryset(self,search_filter):
        qs = get_filtered_data(search_filter)
        return qs
        
    def list(self, request, *args, **kwargs):
        custom_filter = ['unpaid_patient','weekly_amount','monthly_amount','pet_type']
        search_filter = request.data.get('search_filter',None) if request.data else request.query_params
        if search_filter:
            custom_response = [True for filters in search_filter if filters in custom_filter]
            qs = self.get_queryset(search_filter=search_filter)
            if custom_response:
                return Response(data=qs)
            serializer = ApointmentSerializer(qs, many=True)
            return Response(data=serializer.data)
        return Response(data={})

class AppointmentListCreateView(generics.ListCreateAPIView):
    
    queryset = Appointment.objects.all()
    serializer_class = ApointmentSerializer

class AppointmentDetailUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ApointmentSerializer
    
    def get_queryset(self):
        appointment_data = Appointment.objects.all()
        return appointment_data