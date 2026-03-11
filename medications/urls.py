# medications/urls.py
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from medications import views

urlpatterns = [
    path("", views.api_root),
    path("medications/", views.MedicationList.as_view(), name="medication-list"),
    path(
        "medications/<int:pk>/",
        views.MedicationDetail.as_view(),
        name="medication-detail",
    ),
    path(
        "medications/<int:medication_pk>/schedules/",
        views.ScheduleList.as_view(),
        name="schedule-list",
    ),
    path(
        "medications/<int:medication_pk>/schedules/<int:pk>/",
        views.ScheduleDetail.as_view(),
        name="schedule-detail",
    ),
    path(
        "medications/<int:medication_pk>/schedules/<int:schedule_pk>/doselogs/",
        views.DoseLogList.as_view(),
        name="doselog-list",
    ),
    path(
        "medications/<int:medication_pk>/schedules/<int:schedule_pk>/doselogs/<int:pk>/",
        views.DoseLogDetail.as_view(),
        name="doselog-detail",
    ),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("medicines-due/", views.medicines_due, name="medicines-due"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
