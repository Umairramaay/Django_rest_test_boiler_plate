from django.db import models


class Patient(models.Model):
    CAT = "Cat"
    DOG = "Dog"
    BIRD = "Bird"
    PET_TYPES = ((CAT, "Cat"), (DOG, "Dog"),
                  (BIRD, "Bird"))
    
    pet_name =  models.CharField(max_length=55, blank=True, null=True)
    pet_type =  models.CharField(choices=PET_TYPES,max_length=10,null=True,blank=True,default=None,help_text='pet types')
    owner_name =  models.CharField(max_length=55, blank=True, null=True)
    owner_address =  models.TextField(blank=True, null=True)
    owner_phone_number = models.CharField(max_length=12,unique=True,blank=True, null=True)
    
    def __str__(self) -> str:
        return self.pet_name
    

class Appointment(models.Model):
    
    USD = 'USD'
    EURO = 'EURO'
    BITCOIN = 'BITCOIN'
    FREE = 'FREE'
    
    CURRENCY_CHOICES = ((USD, 'USD'),(EURO, 'EURO'),(BITCOIN, 'BITCOIN'),(FREE, 'FREE'))
    patient = models.ForeignKey(Patient,null=True,blank=True,on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True, help_text='Appointment Start Time')
    end_time = models.DateTimeField(null=True, blank=True, help_text='Appointment End Time')
    description =  models.TextField(null=True, blank=True)
    fee_paid = models.DecimalField(decimal_places=2,max_digits=6,help_text='Fee Paid for Appointment',null=True, blank=True)
    billed_amount = models.DecimalField(decimal_places=2,max_digits=6,help_text='Fee for Appointment',null=True, blank=True)
    currency = models.CharField(choices=CURRENCY_CHOICES,max_length=10,default="USD", help_text='currency codes')
    
    def __str__(self) -> str:
        return self.patient.owner_name
    