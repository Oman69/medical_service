from rest_framework import serializers
from .models import Consultation


class ConsultationSerializer(serializers.ModelSerializer):
    doctor_name = serializers.CharField(source='doctor.user.get_full_name', read_only=True)
    patient_name = serializers.CharField(source='patient.user.get_full_name', read_only=True)
    clinic_name = serializers.CharField(source='clinic.name', read_only=True)

    class Meta:
        model = Consultation
        fields = [
            'id', 'created_date', 'start_time', 'end_time', 'status',
            'doctor', 'patient', 'clinic', 'doctor_name', 'patient_name', 'clinic_name'
        ]
        read_only_fields = ['created_date']


class ConsultationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['start_time', 'end_time', 'doctor', 'patient', 'clinic']


class ConsultationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Consultation
        fields = ['status']