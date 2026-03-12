# medications/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Medication, Schedule, DoseLog


class MedicationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Medication model.
    'schedules' is a read-only list of IDs associated with this med.
    """

    owner = serializers.ReadOnlyField(source="owner.username")
    schedules = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Medication
        fields = (
            "id",
            "name",
            "dosage",
            "instructions",
            "is_active",
            "owner",
            "schedules",
            "created",
        )


class ScheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Schedule model.
    You must provide a 'medication' ID and 'start_date' when creating.
    """

    medication_name = serializers.ReadOnlyField(source="medication.name")
    dose_logs = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Schedule
        fields = (
            "id",
            "medication",
            "medication_name",
            "frequency",
            "times_per_day",
            "start_date",
            "end_date",
            "next_dose_time",
            "dose_logs",
        )


class DoseLogSerializer(serializers.ModelSerializer):
    """
    Serializer for logging when a dose was taken.
    """

    medication_name = serializers.ReadOnlyField(source="schedule.medication.name")

    class Meta:
        model = DoseLog
        fields = (
            "id",
            "schedule",
            "medication_name",
            "taken_at",
            "was_taken",
            "notes",
        )


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer to see which medications belong to which user.
    """

    medications = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = User
        fields = (
            "id",
            "username",
            "medications",
        )
