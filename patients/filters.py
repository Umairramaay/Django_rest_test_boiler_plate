from datetime import datetime, timedelta
from django.db.models import Sum, F, Q
from patients.models import Appointment,Patient

def get_filtered_data(filters):
    
    if 'patient' in filters:
        patient_id = filters.get('patient')
        if 'unpaid_patient' in filters:
            return {
                'unpaid_amount':Appointment.objects.filter(patient_id=patient_id) \
                    .aggregate(total = Sum(F('billed_amount')+(-1 *F('fee_paid'))))['total']
            }
        
        return Appointment.objects.filter(patient_id=patient_id)
    
    if 'date' in filters:
        filterd_date = filters.get('date')
        return Appointment.objects.filter(start_time__date=filterd_date)
    
    if 'unpaid' in filters:
        return Appointment.objects.filter(Q(currency=Appointment.FREE) | Q(fee_paid=None))
    
    if 'weekly_amount' in filters or 'monthly_amount' in filters:
        if 'weekly_amount' in filters:
            days = 7
            filterd_date = filters.get('weekly_amount')
        else:
            days = 30
            filterd_date = filters.get('monthly_amount')
        date_range_weekly = datetime.now()
        resp = {}
        week_check = date_range_weekly - timedelta(days=days)
        resp['billed_amount']=Appointment.objects.filter(start_time__lte=date_range_weekly,
                start_time__gte=week_check) \
            .aggregate(Sum('billed_amount'))
        resp['unpaid_amount']=Appointment.objects.filter(start_time__lte=date_range_weekly,
                start_time__gte=week_check) \
            .aggregate(total = Sum(F('billed_amount')+(-1 *F('fee_paid'))))['total']
                
        resp['balance'] = resp['billed_amount']['billed_amount__sum'] - resp['unpaid_amount']
        
        return resp
        
        
    if 'pet_type' in filters:
        resp = {}
        popularity_dict = {}
        popularity_dict['dog']=Patient.objects.filter(pet_type=Patient.DOG).count()
        popularity_dict['cat']=Patient.objects.filter(pet_type=Patient.CAT).count()
        popularity_dict['bird']=Patient.objects.filter(pet_type=Patient.BIRD).count() 
        
        resp['most_popular'] = {
            max(popularity_dict,key = popularity_dict.get):max(popularity_dict.values())
        }
        
        resp['dog_revenue'] = Appointment.objects.filter(patient__pet_type=Patient.DOG) \
                                .aggregate(Sum('billed_amount'))
        resp['cat_revenue'] = Appointment.objects.filter(patient__pet_type=Patient.CAT) \
                                .aggregate(Sum('billed_amount'))
        resp['bird_revenue'] = Appointment.objects.filter(patient__pet_type=Patient.BIRD) \
                                .aggregate(Sum('billed_amount'))
        return resp