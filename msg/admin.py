from django.contrib import admin

from msg.models import Message


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'datetime')


admin.site.register(Message, MessagesAdmin)
