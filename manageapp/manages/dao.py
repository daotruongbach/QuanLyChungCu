from .models import PaymentInvoice, LockerItem
from django.db.models import Sum

def get_total_payment_by_user(user_id):
    return PaymentInvoice.objects.filter(resident_id=user_id).aggregate(total=Sum('amount'))

def create_locker_item(resident, item_name):
    return LockerItem.objects.create(resident=resident, item_name=item_name)


