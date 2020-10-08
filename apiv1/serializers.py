from rest_framework import serializers
from rest_framework.serializers import SerializerMethodField
from schedule.models import *


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'


class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = '__all__'


class StaffSerializer(serializers.ModelSerializer):
    job_id = JobSerializer()
    team_id = TeamSerializer()

    class Meta:
        model = Staff
        fields = '__all__'


class StaffWithShiftScheduleSerializer(serializers.ModelSerializer):
    job_id = JobSerializer()
    team_id = TeamSerializer()

    shifts = SerializerMethodField()

    class Meta:
        model = Staff
        fields = ['name', 'job_id', 'team_id', 'shifts']

    def get_shifts(self, obj):
        try:
            import datetime
            start_date = datetime.date(2020, 9, 1)
            end_date = datetime.date(2020, 9, 30)

            staff = Staff.objects.get(id=obj.id)
            shifts = ShiftSchedule.objects.all().filter(
                staff_id=staff,
                date__range=[start_date, end_date])

            shift_schedule_with_staff = ShiftScheduleSerializer(
                shifts,
                many=True).data
        except:
            shift_schedule_with_staff = None

        return shift_schedule_with_staff


class BaseFimSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fim
        fields = '__all__'


class BaseAvoidTimeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AvoidTime
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    responsible_staff_id = StaffSerializer()
    fim_patient_id = BaseFimSerializer(many=True)
    avoid_patient_id = BaseAvoidTimeSerializer(many=True)

    class Meta:
        model = Patient
        fields = ['id', 'name', 'responsible_staff_id', 'fim_patient_id', 'avoid_patient_id']


class FimSerializer(BaseFimSerializer):
    patient_id = PatientSerializer(read_only=True)
    patient_uid = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)

    def create(self, validated_date):
        validated_date['patient_id'] = validated_date.get('patient_uid', None)
        if validated_date['patient_id'] is None:
            raise serializers.ValidationError("Patient not found.")
        del validated_date['patient_uid']
        return Fim.objects.create(**validated_date)


class AvoidTimeSerializer(BaseAvoidTimeSerializer):
    patient_id = PatientSerializer(read_only=True)
    patient_uid = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)

    def create(self, validated_date):
        validated_date['patient_id'] = validated_date.get('patient_uid', None)
        if validated_date['patient_id'] is None:
            raise serializers.ValidationError("Patient not found.")
        del validated_date['patient_uid']
        return AvoidTime.objects.create(**validated_date)


class ApplyTimeSerializer(serializers.ModelSerializer):
    patient_id = PatientSerializer()
    patient_uid = serializers.PrimaryKeyRelatedField(queryset=Patient.objects.all(), write_only=True)

    class Meta:
        model = ApplyTime
        fields = '__all__'

    def create(self, validated_date):
        validated_date['patient_id'] = validated_date.get('patient_uid', None)

        if validated_date['patient_id'] is None:
            raise serializers.ValidationError("Patient not found.")

        del validated_date['patient_uid']

        return ApplyTime.objects.create(**validated_date)


class ShiftTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShiftType
        fields = '__all__'


class ShiftScheduleSerializer(serializers.ModelSerializer):
    shift_type = ShiftTypeSerializer(read_only=True)
    shift_type_uid = serializers.PrimaryKeyRelatedField(queryset=ShiftType.objects.all(), write_only=True)

    class Meta:
        model = ShiftSchedule
        fields = '__all__'

    def create(self, validated_date):
        validated_date['shift_type'] = validated_date.get('shift_type_uid', None)

        if validated_date['shift_type_uid'] is None:
            raise serializers.ValidationError("shift_type_uid not found.")

        del validated_date['shift_type_uid']

        return ShiftType.objects.create(**validated_date)
