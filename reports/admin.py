from django.contrib import admin

from reports.models import Report, ReportData

admin.site.register(Report)
admin.site.register(ReportData)
