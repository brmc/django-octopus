from django.views.generic.dates import DayArchiveView
from octopus.views import OctopusDetailView, OctopusListView, \
    OctopusDateDetailView, OctopusYearArchiveView, OctopusArchiveIndexView, \
    OctopusDayArchiveView, OctopusWeekArchiveView, OctopusMonthArchiveView, \
    OctopusTodayArchiveView, OctopusCreateView, OctopusUpdateView, \
    OctopusDeleteView
from test_app.models import TestModel


__all__ = ['DetailView', 'ListView', 'SuffixView',
    'DateDetailView', 'YearArchiveView',
    'ArchiveIndexView', 'DayArchiveView', 'WeekArchiveView', 'MonthArchiveView',
    'TodayArchiveView', 'CreateView', 'UpdateView', 'DeleteView']

class DetailView(OctopusDetailView):
    model = TestModel
    template_name = "full.html"
    fragment_name = "fragment.html"


class ListView(OctopusListView):
    model = TestModel
    template_name = "full.html"
    fragment_name = "fragment_list.html"


class SuffixView(OctopusDetailView):
    model = TestModel


class DateDetailView(OctopusDateDetailView):
    model = TestModel
    date_field = 'date'


class YearArchiveView(OctopusYearArchiveView):
    model = TestModel
    date_field = 'date'


class ArchiveIndexView(OctopusArchiveIndexView):
    model = TestModel
    date_field = 'date'


class DayArchiveView(OctopusDayArchiveView):
    model = TestModel
    date_field = 'date'


class WeekArchiveView(OctopusWeekArchiveView):
    model = TestModel
    date_field = 'date'
    week_format = "%W"


class MonthArchiveView(OctopusMonthArchiveView):
    model = TestModel
    date_field = 'date'


class TodayArchiveView(OctopusTodayArchiveView):
    model = TestModel
    date_field = 'date'

edit_views = (OctopusCreateView, OctopusUpdateView, OctopusDeleteView)

for view in edit_views:
    name = view.__name__.replace("Octopus", "")

    locals()[name] = type(name, (view, ), {
        'model': TestModel,
        'success_url': '/list/',
        'fields': ('date', )
    })