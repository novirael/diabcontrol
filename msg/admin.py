from django.contrib import admin

from msg.models import Message, Alert


class MessagesAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'content', 'datetime')


class AlertAdmin(admin.ModelAdmin):
    list_display = ('user', 'content')

admin.site.register(Message, MessagesAdmin)
admin.site.register(Alert, AlertAdmin)
