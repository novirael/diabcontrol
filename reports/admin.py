from django.contrib import admin

from reports.models import Report, ReportData


class ReportDataInline(admin.TabularInline):
    model = ReportData


class ReportAdmin(admin.ModelAdmin):
    list_display = ('date', 'patient', 'mood_level', 'has_headaches', 'other_diseases')
    inlines = (ReportDataInline,)


class ReportDataAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'patient', 'report', 'type', 'group', 'value')


admin.site.register(Report, ReportAdmin)
admin.site.register(ReportData, ReportDataAdmin)
