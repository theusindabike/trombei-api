from django.contrib import admin

from trombei_api.places.models import Place, DirectionUrl


class DirectionUrlsInline(admin.TabularInline):
    model = DirectionUrl


class PlaceModelAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    date_hierarchy = "created_at"
    search_fields = ("name",)
    list_filter = ("created_at",)

    inlines = [DirectionUrlsInline]


admin.site.register(Place, PlaceModelAdmin)
