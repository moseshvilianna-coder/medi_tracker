# medications/views.py
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import User
from rest_framework import generics, permissions
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .models import Medication, Schedule, DoseLog
from .serializers import (
    MedicationSerializer,
    ScheduleSerializer,
    DoseLogSerializer,
    UserSerializer,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "users": reverse("user-list", request=request, format=format),
            "medications": reverse("medication-list", request=request, format=format),
            "medicines-due": reverse("medicines-due", request=request, format=format),
        }
    )


class MedicationList(generics.ListCreateAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Medication.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MedicationDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MedicationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Medication.objects.filter(owner=self.request.user)


class ScheduleList(generics.ListCreateAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(
            medication__owner=self.request.user,
            medication__pk=self.kwargs["medication_pk"],
        )


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(
            medication__owner=self.request.user,
            medication__pk=self.kwargs["medication_pk"],
        )


class DoseLogList(generics.ListCreateAPIView):
    serializer_class = DoseLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoseLog.objects.filter(
            schedule__medication__owner=self.request.user,
            schedule__pk=self.kwargs["schedule_pk"],
        )


class DoseLogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoseLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoseLog.objects.filter(
            schedule__medication__owner=self.request.user,
            schedule__pk=self.kwargs["schedule_pk"],
        )


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


@api_view(["GET"])
def medicines_due(request):
    """
    Returns medications whose next dose is due within the next hour.
    This powers the reminder feature.
    """
    now = timezone.now()
    one_hour_later = now + timedelta(hours=1)

    due_schedules = Schedule.objects.filter(
        medication__owner=request.user,
        next_dose_time__gte=now,
        next_dose_time__lte=one_hour_later,
    )

    serializer = ScheduleSerializer(
        due_schedules, many=True, context={"request": request}
    )
    return Response(serializer.data)
