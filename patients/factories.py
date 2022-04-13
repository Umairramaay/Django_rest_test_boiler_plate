from datetime import datetime, timedelta
import factory
from patients.models import Patient,Appointment

PET_TYPES = [randome_type[0] for randome_type in Patient.PET_TYPES]

class PatientFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Patient
        
    pet_name = factory.Faker('first_name')
    pet_type = factory.Faker('random_element', elements=PET_TYPES)
    owner_name = factory.Faker('user_name')
    owner_phone_number = factory.Sequence(lambda n: f'+112355512{n:02d}')
    owner_address = '555 Random Address'
    

class AppointmentFactory(factory.django.DjangoModelFactory):
    
    class Meta:
        model = Appointment
        
    start_time = factory.Sequence(lambda n: datetime.now() - timedelta(days=1*n))
    end_time = datetime.now()
    description = factory.Faker('first_name')
    fee_paid = factory.Iterator([50,100,80,120])
    billed_amount = factory.Iterator([100,200,120,220])
    patient = factory.SubFactory(PatientFactory)
    currency = "USD"
    
def setup_patients(size=1):
    if size > 1:
        PatientFactory.create_batch(size=size)
    else:
        PatientFactory()
        
def setup_appointments(size=1):
    if size > 1:
        AppointmentFactory.create_batch(size=size)
    else:
        AppointmentFactory()