from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ApartmentViewSet, PaymentInvoiceViewSet, LockerItemViewSet,
                    ComplaintViewSet, SurveyViewSet, SurveyResponseViewSet, UserViewSet)

router = DefaultRouter()
router.register('apartments', ApartmentViewSet, basename='apartment')
router.register('invoices', PaymentInvoiceViewSet, basename='invoice')
router.register('locker-items', LockerItemViewSet, basename='lockeritem')
router.register('complaints', ComplaintViewSet, basename='complaint')
router.register('surveys', SurveyViewSet, basename='survey')
router.register('survey-responses', SurveyResponseViewSet, basename='surveyresponse')
router.register('users', UserViewSet, basename='user')

urlpatterns = [
    path('', include(router.urls))
]
