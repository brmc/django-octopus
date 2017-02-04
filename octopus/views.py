import warnings

from django.views.generic.dates import DateDetailView, YearArchiveView, \
    ArchiveIndexView, DayArchiveView, WeekArchiveView, MonthArchiveView, \
    TodayArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView, View
from django.views.generic.edit import FormView, CreateView, UpdateView, \
    DeleteView

deprecation_msg = "Unless anyone objects, `fragment_name` and " \
                  "`fragment_suffix` will be removed in the next version. " \
                  "You should define `fragment` blocks in your templates " \
                  "instead"

__all__ = [
    'OctopusDetailView', 'OctopusListView', 'OctopusDateDetailView',
    'OctopusYearArchiveView', 'OctopusArchiveIndexView',
    'OctopusDayArchiveView', 'OctopusWeekArchiveView',
    'OctopusMonthArchiveView', 'OctopusTodayArchiveView', 'OctopusCreateView',
    'OctopusUpdateView', 'OctopusDeleteView', 'OctopusTemplateView',
    'OctopusView']

class AjaxResponseMixin(object):
    """ use this to add Octopus functionality to your views

    Be sure to set `parent` to the main class from which you're inheriting
    """
    base_template = 'octopus/ajax.html'
    ajax_template = 'octopus/ajax.html'

    parent = None

    def get_context_data(self, **kwargs):
        context = {}

        if hasattr(self.parent, "get_context_data"):
            context = super(self.parent, self).get_context_data(**kwargs)

        template =  self.ajax_template if self.request.is_ajax() \
            else self.base_template

        context['base_template'] = template

        return context


views = (DetailView, TemplateView, ListView, DateDetailView, TodayArchiveView,
         DayArchiveView, WeekArchiveView, MonthArchiveView, YearArchiveView,
         ArchiveIndexView, FormView, CreateView, UpdateView, DeleteView, View)


# Inject AjaxResponseMixin into each view and tack "Octopus" on to the
# beginning of the class. As the app matures, these definitions will become
# explicit, but for now they will be generated on the fly.
for view in views:
    name = 'Octopus%s' % view.__name__

    locals()[name] = type(name, (AjaxResponseMixin, view), {
        'parent': view
    })
