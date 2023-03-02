from django_filters import (
    FilterSet,
    DateFilter,
    CharFilter,
    ModelChoiceFilter,
)
from rest_framework import filters
from trombei_api.events.models import Event
from trombei_api.places.models import Place


class LoggedUserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class FeedFilter(FilterSet):
    title = CharFilter(field_name="title", lookup_expr="icontains")
    content = CharFilter(field_name="content", lookup_expr="icontains")
    place = ModelChoiceFilter(queryset=Place.objects.all())
    date = DateFilter(field_name="date", lookup_expr="gte")

    class Meta:
        model = Event
        fields = ["title", "content", "place", "date"]
