from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from medications import views

urlpatterns = [
    path("", views.api_root, name="api-root"),
    path("medications/", views.MedicationList.as_view(), name="medication-list"),
    path(
        "medications/<int:pk>/",
        views.MedicationDetail.as_view(),
        name="medication-detail",
    ),
    path("schedules/", views.ScheduleList.as_view(), name="schedule-list"),
    path("schedules/<int:pk>/", views.ScheduleDetail.as_view(), name="schedule-detail"),
    path("doselogs/", views.DoseLogList.as_view(), name="doselog-list"),
    path("doselogs/<int:pk>/", views.DoseLogDetail.as_view(), name="doselog-detail"),
    path("users/", views.UserList.as_view(), name="user-list"),
    path("users/<int:pk>/", views.UserDetail.as_view(), name="user-detail"),
    path("medicines-due/", views.medicines_due, name="medicines-due"),
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]

urlpatterns = format_suffix_patterns(urlpatterns)
