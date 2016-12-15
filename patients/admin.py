from django.contrib import admin

from patients.models import Relationship


class RelationshipAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient')


admin.site.register(Relationship, RelationshipAdmin)
