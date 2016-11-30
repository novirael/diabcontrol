from django.contrib import admin

from msg.models import Message


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'content', 'datetime')


admin.site.register(Message, MessagesAdmin)
