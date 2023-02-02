from django.contrib import admin

from trombei_api.events.models import Event


class EventModelAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'date', 'status', 'created_at', 'owner')
    date_hierarchy = 'created_at'
    search_fields = ('title', 'content', 'date', 'status', 'created_at', 'owner')
    list_filter = ('created_at',)


admin.site.register(Event, EventModelAdmin)
