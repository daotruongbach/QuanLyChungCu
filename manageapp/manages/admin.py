from django.contrib import admin
from .models import User, Apartment, PaymentInvoice, LockerItem, Complaint, Survey, SurveyQuestion, SurveyChoice, SurveyResponse, SurveyAnswer

class ManageApartmentAdmin(admin.AdminSite):
    site_header = "Apartment Administration"
    site_title = "Condo Admin"

admin_site = ManageApartmentAdmin(name='my_admin')

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'role', 'is_active']

@admin.register(Apartment)
class ApartmentAdmin(admin.ModelAdmin):
    list_display = ['number', 'resident', 'floor', 'active']

@admin.register(PaymentInvoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['resident', 'month_year', 'amount', 'pay_method', 'pay_status']

@admin.register(LockerItem)
class LockerItemAdmin(admin.ModelAdmin):
    list_display = ['resident', 'item_name', 'status']

@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['resident', 'title', 'resolve_status']

@admin.register(Survey)
class SurveyAdmin(admin.ModelAdmin):
    list_display = ['title', 'created_by', 'active']

@admin.register(SurveyQuestion)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['question_text', 'survey']

@admin.register(SurveyChoice)
class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['choice_text', 'question']

@admin.register(SurveyResponse)
class ResponseAdmin(admin.ModelAdmin):
    list_display = ['survey', 'resident']

@admin.register(SurveyAnswer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['response', 'question', 'choice']
