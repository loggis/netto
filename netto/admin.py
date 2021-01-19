from django.contrib import admin
from .models import Device
from .models import Log
from import_export.admin import ImportExportModelAdmin

@admin.register(Device)
class DeviceAdmin(ImportExportModelAdmin):
    pass

@admin.register(Log)
class LogAdmin(ImportExportModelAdmin):
    pass




