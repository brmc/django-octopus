from django.views.generic.dates import DayArchiveView
from octopus.views import OctopusDetailView, OctopusListView, \
    OctopusDateDetailView, OctopusYearArchiveView, OctopusArchiveIndexView, \
    OctopusDayArchiveView, OctopusWeekArchiveView, OctopusMonthArchiveView, \
    OctopusTodayArchiveView, OctopusCreateView, OctopusUpdateView, \
    OctopusDeleteView, OctopusTemplateView
from test_app.models import TestModel


__all__ = ['DetailView', 'ListView', 'SuffixView',
    'DateDetailView', 'YearArchiveView',
    'ArchiveIndexView', 'DayArchiveView', 'WeekArchiveView', 'MonthArchiveView',
    'TodayArchiveView', 'CreateView', 'UpdateView', 'DeleteView']

class DetailView(OctopusDetailView):
    model = TestModel
    base_template = 'base.html'
    template_name = 'full_new.html'

class ListView(OctopusListView):
    model = TestModel
    base_template = 'base.html'
    template_name = 'full_list_new.html'

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

OctopusCreateView.fragment_name = 'test_app/full_form.html'

class FragmentView(OctopusTemplateView):
    base_template = 'base.html'
    template_name = 'full_new.html'