from django.contrib import admin
from my_apps.users.models import User, AuditLog
from django.contrib.auth.models import Permission


class CustomUserAdmin(admin.ModelAdmin):
    fields = ['name', 'email', 'phone', 'password', 'is_active', 'is_staff', 'is_superuser', 'groups',
              'user_permissions']
    list_display = ['name', 'email', 'phone', 'is_active', 'is_staff', 'is_superuser']
    search_fields = ['name', 'email', 'phone']


admin.site.register(User, CustomUserAdmin)
admin.site.register(AuditLog)
admin.site.register(Permission)
