from django_filters import FilterSet, AllValuesFilter, ChoiceFilter, DateFilter
from rest_framework import filters

from trombei_api.events.models import Event


class LoggedUserFilter(filters.BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        return queryset.filter(owner=request.user)


class EventFilter(FilterSet):
    from_created_at = DateFilter(field_name='created_at', lookup_expr='gte')
    to_created_at = DateFilter(field_name='created_at', lookup_expr='lte')
    title = AllValuesFilter(field_name='title')
    content = AllValuesFilter(field_name='content')
    status = ChoiceFilter(field_name='status', choices=Event.EventStatus.choices)

    class Meta:
        model = Event
        fields = ['title', 'content', 'status', 'created_at']
