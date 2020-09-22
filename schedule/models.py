import uuid

from django.db import models
from django.utils import timezone


class BaseClass(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    created_at = models.DateTimeField(default=timezone.now)


class Team(BaseClass):
    name = models.CharField(verbose_name='チーム名', max_length=20)

    def __str__(self):
        return f'{self.name}'


class Job(BaseClass):
    name = models.CharField(verbose_name='職種名', max_length=20)

    def __str__(self):
        return f'{self.name}'


class Staff(BaseClass):
    name = models.CharField(max_length=20)
    team_id = models.ForeignKey(Team, related_name='team_id', on_delete=models.PROTECT)
    job_id = models.ForeignKey(Job, related_name='job_id', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name}'


class Patient(BaseClass):
    name = models.CharField(verbose_name='患者氏名', max_length=20)
    responsible_staff_id = models.ForeignKey(Staff, related_name='responsible_staff_id', on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.name} {self.responsible_staff_id.name}'


class Fim(BaseClass):
    patient_id = models.ForeignKey(Patient, related_name='fim_patient_id', on_delete=models.PROTECT)
    meal = models.IntegerField()
    grooming = models.IntegerField()
    bed_bath = models.IntegerField()
    dressing_upper_body = models.IntegerField()
    dressing_lower_body = models.IntegerField()
    toilet_operation = models.IntegerField()
    urination_control = models.IntegerField()
    defecation_control = models.IntegerField()
    bed_chair_wheelchair = models.IntegerField()
    toilet = models.IntegerField()
    bathtub_shower = models.IntegerField()
    walking = models.IntegerField()
    wheelchair = models.IntegerField()
    stairs = models.IntegerField()
    understanding = models.IntegerField()
    front_out = models.IntegerField()
    social_ac = models.IntegerField()
    problem_solving = models.IntegerField()
    memory = models.IntegerField()
    main_move_method = models.TextField()


class AvoidTime(BaseClass):
    patient_id = models.ForeignKey(Patient, related_name='avoid_patient_id', on_delete=models.CASCADE)
    avoid_reason = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.patient_id.name} {self.start_time} - {self.end_time} {self.avoid_reason}'


class ApplyTime(BaseClass):
    patient_id = models.ForeignKey(Patient, related_name='apply_patient_id', on_delete=models.CASCADE)
    apply_reason = models.CharField(max_length=50)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return f'{self.patient_id.name} {self.start_time} - {self.end_time} {self.apply_reason}'


class ShiftType(models.Model):
    type = models.IntegerField(primary_key=True, choices=((1, '日勤'), (2, '公休'), (3, '早番'), (4, '遅番'), (5, '夜勤')))
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.type}: {self.start_time}-{self.end_time}'


class ShiftSchedule(models.Model):
    staff_id = models.ForeignKey(Staff, related_name='staff_id', on_delete=models.CASCADE)
    date = models.DateField()
    shift_type = models.ForeignKey(ShiftType, related_name='shift_type', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date}: {self.staff_id.name}'
