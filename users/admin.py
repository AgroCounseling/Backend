from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from categories.admin import CategoryConsultantInline
from .models import *

admin.site.site_header = "Агро Консультирование"
admin.site.site_title = "Агро Консультирование"
admin.site.index_title = "Агро Консультирование"


class ImageConsultantAdmin(admin.ModelAdmin):
    fields = ('certificate_tag',)
    readonly_fields = ('certificate_tag',)


class ImageConsultantInline(admin.TabularInline):
    model = ImageConsultant
    fields = ('certificate_tag', 'certificate_image')
    readonly_fields = ('certificate_tag',)

    def get_extra(self, request, obj=None, **kwargs):
        if obj is None:
            return self.extra
        return 0


class ConsultantAdmin(admin.ModelAdmin):
    inlines = (CategoryConsultantInline, ImageConsultantInline)
    list_display = ('user', 'get_consultant', 'short_description')
    fields = (
    'user', 'get_consultant', 'title_ru', 'title_kg', 'description_ru', 'description_kg', 'comment_ru', 'comment_kg')
    list_filter = ['user__email', 'user__first_name', 'user__last_name', 'user__is_active']
    search_fields = ['user__email', 'user__first_name', 'user__last_name']
    readonly_fields = ('get_consultant',)

    def get_consultant(self, obj):
        return 'Имя:\t{}\n\n' \
               'Фамилия:\t{}\n\n' \
               'Телефон:\t{}\n\n'.format(obj.user.first_name, obj.user.last_name, obj.user.phone)

    get_consultant.short_description = 'Информация о консультанте'


class UserAdmin(UserAdmin):
    model = User
    list_display = (
        'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_client', 'is_consultant', 'is_superuser')
    fieldsets = (
        (None, {'fields': (
            'email', 'first_name', 'last_name', 'phone', 'is_active', 'is_client', 'is_consultant',
            'date_joined')}),
    )
    ordering = ('email',)
    list_filter = ['email', 'first_name', 'last_name', 'is_active', 'is_client', 'is_consultant']
    search_fields = ['email', 'first_name', 'last_name']
    readonly_fields = ['date_joined']

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'first_name', 'last_name', 'password1', 'password2', 'phone', 'is_active',
                'is_client', 'is_consultant',
            )}
         ),
    )


class RatingStartAdmin(admin.ModelAdmin):
    list_display = ['id', 'value']
    list_filter = ['value']
    search_fields = ['value']


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['consultant', 'text', 'name', 'email', 'star']
    fields = ['consultant', 'get_consultant', 'name', 'email', 'text_ru', 'text_kg', 'star']
    list_filter = ['consultant__user__email', 'consultant__user__first_name', 'consultant__user__last_name']
    search_fields = ['consultant__user__email', 'consultant__user__first_name', 'consultant__user__last_name']
    readonly_fields = ['get_consultant']

    def get_consultant(self, obj):
        return 'Имя:\t{}\n\n' \
               'Фамилия:\t{}\n\n' \
               'Телефон:\t{}\n\n'.format(obj.consultant.user.first_name, obj.consultant.user.last_name,
                                         obj.consultant.user.phone)

    get_consultant.short_description = 'Информация о консультанте'


admin.site.register(User, UserAdmin)
admin.site.register(RatingStart, RatingStartAdmin)
admin.site.register(Consultant, ConsultantAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.unregister(Group)
