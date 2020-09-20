from rest_framework import serializers
from schedule.models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    staff = serializers.StringRelatedField(many=True)
    class Meta:
        model = Patient
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = Staff
        fields = '__all__'


class AvoidTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvoidTime
        fields = '__all__'


class ApplyTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class ShiftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftType
        fields = '__all__'


class ShiftScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftSchedule
        fields = '__all__'
