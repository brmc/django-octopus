from django.views.generic.dates import DayArchiveView
from octopus.views import OctopusDetailView, OctopusListView, \
    OctopusDateDetailView, OctopusYearArchiveView, OctopusArchiveIndexView, \
    OctopusDayArchiveView, OctopusWeekArchiveView, OctopusMonthArchiveView, \
    OctopusTodayArchiveView
from test_app.models import TestModel


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
