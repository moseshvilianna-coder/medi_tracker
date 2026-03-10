# medications/serializers.py
from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Medication, Schedule, DoseLog


class MedicationSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    schedules = serializers.HyperlinkedRelatedField(
        many=True, view_name="schedule-detail", read_only=True
    )

    class Meta:
        model = Medication
        fields = (
            "url",
            "id",
            "name",
            "dosage",
            "instructions",
            "is_active",
            "owner",
            "schedules",
            "created",
        )


class ScheduleSerializer(serializers.HyperlinkedModelSerializer):
    medication = serializers.ReadOnlyField(source="medication.name")
    dose_logs = serializers.HyperlinkedRelatedField(
        many=True, view_name="doselog-detail", read_only=True
    )

    class Meta:
        model = Schedule
        fields = (
            "url",
            "id",
            "medication",
            "frequency",
            "times_per_day",
            "start_date",
            "end_date",
            "next_dose_time",
            "dose_logs",
        )


class DoseLogSerializer(serializers.HyperlinkedModelSerializer):
    schedule = serializers.ReadOnlyField(source="schedule.medication.name")

    class Meta:
        model = DoseLog
        fields = (
            "url",
            "id",
            "schedule",
            "taken_at",
            "was_taken",
            "notes",
        )


class UserSerializer(serializers.HyperlinkedModelSerializer):
    medications = serializers.HyperlinkedRelatedField(
        many=True, view_name="medication-detail", read_only=True
    )

    class Meta:
        model = User
        fields = (
            "url",
            "id",
            "username",
            "medications",
        )
