from django.contrib import admin

from .models import Client, Department, Settings


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ['user', 'id', 'permission_level']
    fields = ['id', 'user', 'permission_level', 'department']
    readonly_fields = ['id']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'employees']
    fields = ['name', 'employees']
    readonly_fields = ['employees']


@admin.register(Settings)
class SettingsAdmin(admin.ModelAdmin):
    list_display = ['prefix', 'client']
    fields = ['prefix', 'client']
