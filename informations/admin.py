from django.contrib import admin
from .models import *

admin.site.site_header = "Агро Консультирование"
admin.site.site_title = "Агро Консультирование"
admin.site.index_title = "Агро Консультирование"


class PhoneInfoAdmin(admin.TabularInline):
    model = PhonesInfo
    fields = ('phone', 'address')

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return self.extra
        return 0


class ContactInfoAdmin(admin.ModelAdmin):
    list_display = ['address']
    list_filter = ['address']
    inlines = [PhoneInfoAdmin]


admin.site.register(Slider)
admin.site.register(ContactInfo, ContactInfoAdmin)
