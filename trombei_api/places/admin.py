from django.contrib import admin

from trombei_api.places.models import Place


class PlaceModelAdmin(admin.ModelAdmin):
    list_display = ("name", "owner")
    date_hierarchy = "created_at"
    search_fields = ("name",)
    list_filter = ("created_at",)


admin.site.register(Place, PlaceModelAdmin)
