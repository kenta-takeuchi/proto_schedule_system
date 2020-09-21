from django.urls import path, include

from rest_framework import routers

from . import views

router = routers.SimpleRouter()
router.register('teams', views.TeamViewSet)
router.register('jobs', views.JobViewSet)
router.register('staff', views.StaffViewSet)
router.register('patients', views.PatientViewSet)
router.register('fims', views.FimViewSet)
router.register('avoid_times', views.AvoidTimeViewSet)
router.register('apply_times', views.ApplyTimeViewSet)
router.register('shift_types', views.ShiftTypeViewSet)
router.register('shift_schedules', views.ShiftScheduleViewSet)


app_name = 'schedule'
urlpatterns = [
    path('', include(router.urls)),
    path('detail_articles/', views.StaffWithShiftScheduleSerializer.as_view())
]
