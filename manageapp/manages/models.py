from django.db import models
from django.contrib.auth.models import AbstractUser

# Custom user
class User(AbstractUser):
    # Thêm role phân biệt admin/cư dân, hoặc xài group/permission DRF
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('resident', 'Resident'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='resident')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/', null=True, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)

    def __str__(self):
        return self.username

class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True, null=True)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    class Meta:
        abstract = True
        ordering = ['-id']

class Apartment(BaseModel):
    # Mỗi apartment thuộc 1 user (resident), admin có thể thay đổi
    resident = models.OneToOneField(User, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name='apartment')
    number = models.CharField(max_length=50, unique=True)
    floor = models.IntegerField(default=1)

    def __str__(self):
        return f"Apartment {self.number}"

class PaymentInvoice(BaseModel):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='invoices')
    month_year = models.CharField(max_length=7)  # "01/2024"
    amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    PROOF_METHODS = (
        ('transfer', 'Bank Transfer'),
        ('online', 'Online Payment'),
    )
    pay_method = models.CharField(max_length=20, choices=PROOF_METHODS)
    pay_proof = models.ImageField(upload_to='payments/%Y/%m/', null=True, blank=True)
    pay_status = models.CharField(max_length=20, default='pending')  # pending, confirmed, rejected

    def __str__(self):
        return f"Invoice {self.month_year} - {self.resident.username}"

class LockerItem(BaseModel):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locker_items')
    item_name = models.CharField(max_length=100)
    status = models.CharField(max_length=20, default='pending')  # pending, received

    def __str__(self):
        return f"{self.item_name} - {self.resident.username}"

class Complaint(BaseModel):
    resident = models.ForeignKey(User, on_delete=models.CASCADE, related_name='complaints')
    title = models.CharField(max_length=200)
    content = models.TextField()
    resolve_status = models.CharField(max_length=20, default='open')  # open, in_progress, closed

    def __str__(self):
        return f"{self.title} - {self.resident.username}"

class Survey(BaseModel):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_surveys')

    def __str__(self):
        return self.title

class SurveyQuestion(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='questions')
    question_text = models.CharField(max_length=255)

    def __str__(self):
        return self.question_text

class SurveyChoice(BaseModel):
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE, related_name='choices')
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        return self.choice_text

class SurveyResponse(BaseModel):
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE, related_name='responses')
    resident = models.ForeignKey(User, on_delete=models.CASCADE)

class SurveyAnswer(BaseModel):
    response = models.ForeignKey(SurveyResponse, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(SurveyQuestion, on_delete=models.CASCADE)
    choice = models.ForeignKey(SurveyChoice, null=True, blank=True, on_delete=models.SET_NULL)
    answer_text = models.TextField(null=True, blank=True)
