from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from .models import Consultation
from .serializers import (
    ConsultationSerializer,
    ConsultationCreateSerializer,
    ConsultationStatusSerializer
)
from .permissions import IsAdmin, IsDoctor, IsPatient, IsOwnerOrAdmin


class ConsultationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ['status']
    ordering_fields = ['created_date', 'start_time']
    ordering = ['-created_date']
    search_fields = [
        'doctor__user__first_name',
        'doctor__user__last_name',
        'patient__user__first_name',
        'patient__user__last_name'
    ]

    def get_queryset(self):
        user = self.request.user

        if user.role == 'admin':
            return Consultation.objects.all()
        elif user.role == 'doctor':
            return Consultation.objects.filter(doctor__user=user)
        elif user.role == 'patient':
            return Consultation.objects.filter(patient__user=user)

        return Consultation.objects.none()

    def get_serializer_class(self):
        if self.action == 'create':
            return ConsultationCreateSerializer
        elif self.action == 'update_status':
            return ConsultationStatusSerializer
        return ConsultationSerializer

    def get_permissions(self):
        if self.action in ['create']:
            self.permission_classes = [IsAuthenticated, IsPatient]
        elif self.action in ['update', 'partial_update', 'destroy']:
            self.permission_classes = [IsAuthenticated, IsOwnerOrAdmin]
        elif self.action in ['update_status']:
            self.permission_classes = [IsAuthenticated, IsDoctor | IsAdmin]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        consultation = self.get_object()
        serializer = self.get_serializer(consultation, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
