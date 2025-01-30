from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import (User, Apartment, PaymentInvoice, LockerItem, Complaint,
                     Survey, SurveyQuestion, SurveyChoice, SurveyResponse, SurveyAnswer)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'role', 'avatar', 'phone_number', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        # Tự mã hoá password
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class ApartmentSerializer(serializers.ModelSerializer):
    resident_username = serializers.CharField(source='resident.username', read_only=True)
    class Meta:
        model = Apartment
        fields = ['id', 'number', 'floor', 'active', 'resident', 'resident_username']

class PaymentInvoiceSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source='resident.username', read_only=True)

    class Meta:
        model = PaymentInvoice
        fields = ['id', 'resident', 'resident_name', 'month_year', 'amount',
                  'pay_method', 'pay_proof', 'pay_status', 'created_date']

class LockerItemSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source='resident.username', read_only=True)

    class Meta:
        model = LockerItem
        fields = ['id', 'resident', 'resident_name', 'item_name', 'status', 'created_date']

class ComplaintSerializer(serializers.ModelSerializer):
    resident_name = serializers.CharField(source='resident.username', read_only=True)

    class Meta:
        model = Complaint
        fields = ['id', 'resident', 'resident_name', 'title', 'content', 'resolve_status', 'created_date']

class SurveyChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyChoice
        fields = ['id', 'choice_text']

class SurveyQuestionSerializer(serializers.ModelSerializer):
    choices = SurveyChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = SurveyQuestion
        fields = ['id', 'question_text', 'choices']

class SurveySerializer(serializers.ModelSerializer):
    questions = SurveyQuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Survey
        fields = ['id', 'title', 'description', 'created_by', 'questions', 'created_date']

class SurveyAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveyAnswer
        fields = ['id', 'question', 'choice', 'answer_text']

class SurveyResponseSerializer(serializers.ModelSerializer):
    answers = SurveyAnswerSerializer(many=True, write_only=True)

    class Meta:
        model = SurveyResponse
        fields = ['id', 'survey', 'resident', 'answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers', [])
        response = SurveyResponse.objects.create(**validated_data)
        for ans in answers_data:
            SurveyAnswer.objects.create(response=response, **ans)
        return response
