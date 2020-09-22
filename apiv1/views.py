from rest_framework import generics
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .serializers import *


def results(request):
    from django.http import HttpResponse
    from schedule.schedule_service import ScheduleService
    ScheduleService(30).generate_schedule()
    response = "You're looking at the results of question."
    return HttpResponse(response)


class BaseScheduleViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]


class TeamViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class JobViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = Job.objects.all()
    serializer_class = JobSerializer


class PatientViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer


class FimViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""
    queryset = Fim.objects.all()
    serializer_class = FimSerializer


class StaffViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = Staff.objects.all()
    serializer_class = StaffSerializer


class AvoidTimeViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = AvoidTime.objects.all()
    serializer_class = AvoidTimeSerializer


class ApplyTimeViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = ApplyTime.objects.all()
    serializer_class = ApplyTimeSerializer


class ShiftTypeViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = ShiftType.objects.all()
    serializer_class = ShiftTypeSerializer


class ShiftScheduleViewSet(BaseScheduleViewSet):
    """チームのCRUD用汎用API"""

    queryset = ShiftSchedule.objects.all()
    serializer_class = ShiftScheduleSerializer


class StaffWithShiftScheduleSerializer(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Staff.objects.all()
    serializer_class = StaffWithShiftScheduleSerializer
