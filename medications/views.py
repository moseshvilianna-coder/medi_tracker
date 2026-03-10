# medications/views.py
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
            "schedules": reverse("schedule-list", request=request, format=format),
            "dose-logs": reverse("doselog-list", request=request, format=format),
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
        return Schedule.objects.filter(medication__owner=self.request.user)


class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ScheduleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Schedule.objects.filter(medication__owner=self.request.user)


class DoseLogList(generics.ListCreateAPIView):
    serializer_class = DoseLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoseLog.objects.filter(schedule__medication__owner=self.request.user)


class DoseLogDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DoseLogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return DoseLog.objects.filter(schedule__medication__owner=self.request.user)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
