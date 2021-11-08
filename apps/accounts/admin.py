from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Account


class AccountAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'last_login', 'date_joined', 'is_active')
    list_display_links = ('email', 'first_name', 'last_name')
    readonly_fields = ('last_login', 'date_joined')
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# class UserProfileAdmin(admin.ModelAdmin):
#     def thumbnail(self, object):
#         if object.profile_avatar:
#             return format_html('<img src={} width="30" style="border-radius:50%">'.format(
#                 object.profile_avatar.url))
#
#     thumbnail.short_description = 'Profile avatar'
#     list_display = ('thumbnail', 'user', 'country', 'state', 'city')


admin.site.register(Account, AccountAdmin)
# admin.site.register(UserProfile, UserProfileAdmin)
