from django.contrib import admin
from .models import TaskList, Programs


admin.site.register(Programs)
admin.site.register(TaskList)