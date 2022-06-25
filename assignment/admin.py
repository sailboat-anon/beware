from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Assignment, Task

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    pass

class TaskAdmin(SummernoteModelAdmin):
    summernote_fields = 'detail'

admin.site.register(Task, TaskAdmin)