from django.contrib import admin

# Register your models here.

from django.contrib import admin


from .models import *

admin.site.register(Team)
admin.site.register(Job)
admin.site.register(Staff)
admin.site.register(Patient)
admin.site.register(Fim)
admin.site.register(AvoidTime)
admin.site.register(ApplyTime)
admin.site.register(ShiftType)
admin.site.register(ShiftSchedule)

