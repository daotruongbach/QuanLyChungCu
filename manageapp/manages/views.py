from rest_framework import viewsets, generics, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (Apartment, PaymentInvoice, LockerItem, Complaint,
                     Survey, SurveyQuestion, SurveyChoice, SurveyResponse, User)
from . import serializers, paginators, perms, dao

class ApartmentViewSet(viewsets.ViewSet, generics.ListAPIView, generics.RetrieveAPIView):
    queryset = Apartment.objects.filter(active=True)
    serializer_class = serializers.ApartmentSerializer
    pagination_class = paginators.DefaultPagination

    @action(methods=['post'], detail=True, url_path='transfer-ownership', permission_classes=[perms.IsAdminOrReadOnly])
    def transfer_ownership(self, request, pk):
        """
        Ví dụ: Admin chuyển quyền sở hữu apartment sang user khác => resident cũ bị khóa
        """
        apt = self.get_object()
        new_user_id = request.data.get('new_resident_id')
        try:
            new_user = User.objects.get(pk=new_user_id, role='resident')
            if apt.resident:
                old_resident = apt.resident
                old_resident.is_active = False
                old_resident.save()
            apt.resident = new_user
            apt.save()
            return Response({'status': 'transferred'}, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({'error': 'User not found or not resident'}, status=status.HTTP_400_BAD_REQUEST)

class PaymentInvoiceViewSet(viewsets.ModelViewSet):
    queryset = PaymentInvoice.objects.all()
    serializer_class = serializers.PaymentInvoiceSerializer
    pagination_class = paginators.DefaultPagination

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        # Gán resident = user đang đăng nhập (nếu logic là user tự create)
        serializer.save(resident=self.request.user)

class LockerItemViewSet(viewsets.ModelViewSet):
    queryset = LockerItem.objects.all()
    serializer_class = serializers.LockerItemSerializer

    def get_permissions(self):
        # Admin có thể thêm item, update status
        # Resident có thể xem (list, retrieve) => filter theo user
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), perms.IsAdminOrReadOnly()]
        return [permissions.IsAuthenticated()]

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'resident':
            qs = qs.filter(resident=self.request.user)
        return qs

    @action(methods=['post'], detail=True, url_path='receive')
    def mark_received(self, request, pk):
        """Resident confirm đã nhận locker item"""
        item = self.get_object()
        if item.resident == request.user or request.user.role == 'admin':
            item.status = 'received'
            item.save()
            return Response({'status': 'Item received'}, status=status.HTTP_200_OK)
        return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)

class ComplaintViewSet(viewsets.ModelViewSet):
    queryset = Complaint.objects.all()
    serializer_class = serializers.ComplaintSerializer

    def get_queryset(self):
        # Resident chỉ xem complaint của mình
        # Admin xem tất cả
        if self.request.user.is_authenticated and self.request.user.role == 'resident':
            return self.queryset.filter(resident=self.request.user)
        return self.queryset

    def get_permissions(self):
        if self.action in ['create']:
            return [permissions.IsAuthenticated()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated(), perms.IsOwnerOrAdmin()]
        else:
            return [permissions.AllowAny()]

class SurveyViewSet(viewsets.ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = serializers.SurveySerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            # Admin tạo, cập nhật, xóa survey
            return [permissions.IsAuthenticated(), perms.IsAdminOrReadOnly()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=True, url_path='results')
    def get_survey_results(self, request, pk):
        """
        Lấy kết quả (thống kê) cho 1 survey => admin xem
        """
        survey = self.get_object()
        # Tuỳ ý code logic dao ở dao.py
        responses = survey.responses.count()
        return Response({'survey': survey.title, 'total_responses': responses})

class SurveyResponseViewSet(viewsets.ModelViewSet):
    queryset = SurveyResponse.objects.all()
    serializer_class = serializers.SurveyResponseSerializer

    def perform_create(self, serializer):
        # Gán resident là user đăng nhập
        serializer.save(resident=self.request.user)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            # Admin xem danh sách user
            return [permissions.IsAuthenticated(), perms.IsAdminOrReadOnly()]
        return [permissions.AllowAny()]

    @action(methods=['post'], detail=False, url_path='change-password')
    def change_password(self, request):
        user = request.user
        old_pass = request.data.get('old_password')
        new_pass = request.data.get('new_password')
        if not user.check_password(old_pass):
            return Response({'error': 'Old password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
        user.set_password(new_pass)
        user.save()
        return Response({'status': 'Password changed'})
