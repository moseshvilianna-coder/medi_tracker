from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

FREQUENCY_CHOICES = [
    ("daily", "Daily"),
    ("twice_daily", "Twice Daily"),
    ("three_times_daily", "Three Times Daily"),
    ("weekly", "Weekly"),
    ("as_needed", "As Needed"),
]


class Medication(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    instructions = models.TextField(blank=True, default="")
    is_active = models.BooleanField(default=True)
    owner = models.ForeignKey(
        "auth.User", related_name="medications", on_delete=models.CASCADE
    )

    class Meta:
        ordering = ("created",)

    def __str__(self):
        return f"{self.name} ({self.dosage})"


class Schedule(models.Model):
    medication = models.ForeignKey(
        Medication, related_name="schedules", on_delete=models.CASCADE
    )
    frequency = models.CharField(
        choices=FREQUENCY_CHOICES, default="daily", max_length=50
    )
    times_per_day = models.PositiveIntegerField(default=1)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    next_dose_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ("next_dose_time",)

    def save(self, *args, **kwargs):
        """
        Auto-compute next_dose_time based on frequency,
        following the same custom save() pattern as thr Snippet model.
        """
        now = timezone.now()
        if self.frequency == "daily":
            self.next_dose_time = now + timedelta(hours=24)
        elif self.frequency == "twice_daily":
            self.next_dose_time = now + timedelta(hours=12)
        elif self.frequency == "three_times_daily":
            self.next_dose_time = now + timedelta(hours=8)
        elif self.frequency == "weekly":
            self.next_dose_time = now + timedelta(weeks=1)
        else:
            self.next_dose_time = None
        super(Schedule, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.medication.name} - {self.frequency}"


class DoseLog(models.Model):
    schedule = models.ForeignKey(
        Schedule, related_name="dose_logs", on_delete=models.CASCADE
    )
    taken_at = models.DateTimeField(auto_now_add=True)
    was_taken = models.BooleanField(default=False)
    notes = models.CharField(max_length=300, blank=True, default="")

    class Meta:
        ordering = ("-taken_at",)

    def __str__(self):
        status = "taken" if self.was_taken else "missed"
        return f"{self.schedule.medication.name} - {status} at {self.taken_at}"
