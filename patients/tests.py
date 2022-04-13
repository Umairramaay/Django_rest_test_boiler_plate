from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase

from patients.factories import PatientFactory, AppointmentFactory

class PatientsTests(APITestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.patient = PatientFactory()
        self.patient_list_url = reverse('patients-list')
        self.patient_detail_url = reverse('patients-detail',args=[1])
        self.patient_mutate_url = '/api/pets/'
        
    def test_list_patient(self):
        response = self.client.get(self.patient_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_detail_patient(self):
        response = self.client.get(self.patient_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_create_patient(self):
        data = {
            "pet_name":"dummy",
            "pet_type":"Dog",
            "owner_name":"test",
            "owner_address":"unknown",
            "owner_phone_number":+123445678901,
        }
        response = self.client.post(self.patient_mutate_url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_patient(self):
        test_id = self.patient.id
        data = {
            "pet_name":'changed'
        }
        response = self.client.put(self.patient_mutate_url + str(test_id)+'/',data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_delete_patient(self):
        test_id = self.patient.id
        response = self.client.put(self.patient_mutate_url + str(test_id)+'/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        

class AppointmentTests(APITestCase):
    
    def setUp(self) -> None:
        super().setUp()
        self.client = APIClient()
        self.patient = PatientFactory()
        self.appointment = AppointmentFactory()
        self.appointment_url = reverse('appointment',args=[1])
        self.appointment_create_url = reverse('appointment-list-create')
        self.patient_appointment_url = reverse('appointment',args=[1])
        self.appointment_filter_url = reverse('appointment-filters')
        
    def test_create_appointment(self):
        test_id = self.patient.id
        data = {
            "patient":test_id,
            "description":"adfasfa"
        }
        response = self.client.post(self.appointment_create_url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
    def test_update_appointment_detail(self):

        test_id = self.appointment.id
        put_patient_appointment_url = reverse('appointment',args=[test_id])
        data = {
            "description":'changed'
        }
        response = self.client.put(put_patient_appointment_url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_all_appointment_single_patient(self):
        response = self.client.get(self.patient_appointment_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_all_unpaid_appointments(self):
        AppointmentFactory(fee_paid=None) #Dummy Unpaid Appointment
        data = {
            "search_filter":True,
            "unpaid":True
        }
        response = self.client.get(self.appointment_filter_url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_all_unpaid_appointments(self):
        data = {
            "search_filter":True,
            "pet_type":True
            
        }
        response = self.client.get(self.appointment_filter_url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_remaining_bill_patient(self):
        AppointmentFactory(patient=self.patient, billed_amount=100,fee_paid=30) #A Patient to get remaining bill if there is
        data = {
            "search_filter":True,
            "patient":self.patient.id,
            "unpaid_patient":True
        }
        response = self.client.get(self.appointment_filter_url,data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
