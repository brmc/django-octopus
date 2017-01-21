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
    base_template = u'octopus/ajax.html'
    ajax_template = u'octopus/ajax.html'

    parent = None

    # Deprecated
    fragment_name = None
    fragment_suffix = None

    def get_context_data(self, **kwargs):
        context = {}

        if hasattr(self.parent, "get_context_data"):
            context = super(self.parent, self).get_context_data(**kwargs)

        template =  self.ajax_template if self.request.is_ajax() \
            else self.base_template

        context['base_template'] = template

        return context


    def get_legacy_template_names(self, *args, **kwargs):
        warnings.warn(deprecation_msg, DeprecationWarning)
        if self.fragment_suffix is None:
            self.fragment_suffix = '_fragment'

        if self.request.is_ajax():
            if self.fragment_name is not None:
                self.template_name = self.fragment_name
            self.template_name_suffix += self.fragment_suffix

        if hasattr(self.parent, "get_template_names"):
            return super(self.parent, self).get_template_names()

        return [self.template_name, "%s%s"
                % (self.template_name, self.template_name_suffix)]


    def get_template_names(self):
        if self.fragment_name is not None or self.fragment_suffix is not None:
            return self.get_legacy_template_names()

        if hasattr(self.parent, "get_template_names"):
            return super(self.parent, self).get_template_names()

        # hrm...I wonder why i did this...
        return [self.template_name, "%s%s"
                % (self.template_name, self.template_name_suffix)]


class OctopusTemplateView(TemplateView):
    base_template = 'octopus/ajax.html'
    ajax_template = 'octopus/ajax.html'

    fragment_name = None
    fragment_suffix = None

    def get_context_data(self, **kwargs):
        template =  self.ajax_template if self.request.is_ajax() \
            else self.base_template

        return {'base_template': template}

    def get_template_names(self):
        if self.fragment_name is not None or self.fragment_suffix is not None:
            return self.get_legacy_template_names()

        return [self.template_name]

    def get_legacy_template_names(self):
        warnings.warn(deprecation_msg, DeprecationWarning)
        if not self.request.is_ajax():
            return [self.template_name, ]

        if self.fragment_name is not None:
            self.template_name = self.fragment_name
        else:
            self.template_name = self.template_name.replace(
                ".", self.fragment_suffix + ".")


views = (DetailView, ListView, DateDetailView, TodayArchiveView,
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
