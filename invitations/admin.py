from django.contrib import admin

from invitations.models import Invitation


class InvitationAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'doctor', 'patient', 'is_accepted')


admin.site.register(Invitation, InvitationAdmin)
