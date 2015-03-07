from django.views.generic.dates import DateDetailView, YearArchiveView, \
    ArchiveIndexView, DayArchiveView, WeekArchiveView, MonthArchiveView, \
    TodayArchiveView
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView


class AjaxResponseMixin(object):
    fragment_name = None
    fragment_suffix = '_fragment'

    def get_template_names(self):
        if self.request.is_ajax():
            if self.fragment_name is not None:
                self.template_name = self.fragment_name
            self.template_name_suffix += self.fragment_suffix

        if hasattr(self.parent, "get_template_names"):
            return super(self.parent, self).get_template_names()

        return [self.template_name, "%s%s"
                % (self.template_name, self.template_name_suffix)]

views = (DetailView, ListView, DateDetailView, TodayArchiveView,
         DayArchiveView, WeekArchiveView, MonthArchiveView, YearArchiveView,
         ArchiveIndexView)


# Inject AjaxResponseMixin into each view and tack "Octopus" on to the
# beginning of the class .
for view in views:
    name = 'Octopus%s' % view.__name__

    locals()[name] = type(name, (AjaxResponseMixin, view), {
        'parent': view
    })