import json
from datetime import datetime

from django.conf import settings
from django.contrib import admin

from django.contrib.sessions.models import Session

from core.models import AuthenticationAudit


class SessionAdmin(admin.ModelAdmin):

    @staticmethod
    def _session_data(obj):
        return json.dumps(obj.get_decoded(), sort_keys=True)

    @staticmethod
    def created_date(obj):
        return obj.expire_date - datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)

    list_display = ["session_key", "created_date", "expire_date", "_session_data"]
    list_display_links = ["session_key", "created_date", "expire_date", "_session_data"]
    search_fields = ["session_key"]
    readonly_fields = ["session_key", "created_date", "_session_data"]
    fieldsets = [
        ("Session Information", {
            "fields": ["session_key", "created_date", "expire_date"],
            "classes": ["wide"]
        }),
        ("Session Decoded Information", {
            "fields": ["_session_data"],
            "classes": ["wide"]
        })
    ]


class AuthenticationAuditAdmin(admin.ModelAdmin):
    list_display = ["timestamp", "person", "ip_address"]
    list_display_links = ["timestamp", "person", "ip_address"]
    search_fields = ["timestamp", "person", "ip_address"]
    readonly_fields = ["timestamp", "person", "ip_address"]
    fieldsets = [
        ("Date Information", {
            "fields": ["timestamp"],
            "classes": ["wide"]
        }),
        ("User Information", {
            "fields": ["person", "ip_address"],
            "classes": ["wide"]
        })
    ]


class AuditAdmin(admin.ModelAdmin):
    list_display = ["created", "created_by", "person", "action"]
    list_display_links = ["created", "created_by", "person", "action"]
    list_filter = ["action"]
    search_fields = ["person__first_name", "person__last_name"]
    autocomplete_fields = ["person"]
    readonly_fields = [
        "created", "created_by", "person", "action", "original", "current"
    ]
    fieldsets = [
        ("Date Information", {
            "fields": ["created"],
            "classes": ["wide"]
        }),
        ("People Information", {
            "fields": ["created_by", "person"],
            "classes": ["wide"]
        }),
        ("Audit Information", {
            "fields": ["action"],
            "classes": ["wide"]
        }),
        ("Original Information", {
            "fields": ["original"],
            "classes": ["wide"]
        }),
        ("Current Information", {
            "fields": ["current"],
            "classes": ["wide"]
        })
    ]

    @admin.display(description="Created By")
    def created_by_profile(self, instance):
        return instance.created_by.get_full_name()


admin.site.register(Session, SessionAdmin)
admin.site.register(AuthenticationAudit, AuthenticationAuditAdmin))
