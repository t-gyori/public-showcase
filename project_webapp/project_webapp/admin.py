"""
Ez az app nincs benne az app listában, ezért külön meg kell hívni
egy aktív app admin.py fájljából ezen fájl tartalmát, hogy látható
legyenek az itt leírt model adminok az admin menüben.
"""

from django.contrib import admin
from django.contrib.admin.models import LogEntry


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    save_as = True
    date_hierarchy = 'action_time'
    list_filter = ['content_type']
    list_display = ("id", "__str__", "content_type",
                    "action_flag", "user", "action_time",)
    list_display_links = ("__str__", )
    search_fields = list_display
    readonly_fields = ()
    fieldsets = ()

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return True

    def has_delete_permission(self, request, obj=None):
        return False

    def has_view_permission(self, request, obj=None):
        return True
