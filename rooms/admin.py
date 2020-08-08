from django.contrib import admin
from .models import *

admin.site.site_header = "Агро Консультирование"
admin.site.site_title = "Агро Консультирование"
admin.site.index_title = "Агро Консультирование"


class ChatMessageInline(admin.TabularInline):
    model = ChatMessage
    fields = ('thread', 'user', 'message', 'timestamp')
    readonly_fields = ['timestamp']

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return self.extra
        return 0


class ThreadAdmin(admin.ModelAdmin):
    list_display = ['first', 'second', 'time', 'access', 'timestamp']
    list_filter = ['first', 'second', 'time', 'access', ]
    raw_id_fields = ['first', 'second']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    inlines = [ChatMessageInline]


admin.site.register(Thread, ThreadAdmin)
