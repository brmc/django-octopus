from django.core.exceptions import ImproperlyConfigured
from django.views.generic.detail import DetailView, \
    SingleObjectTemplateResponseMixin
from django.views.generic.list import ListView
from django.views.generic.base import TemplateResponseMixin


class AjaxDetailResponseMixin(SingleObjectTemplateResponseMixin):
    fragment_name = None
    def get_template_names(self):
        """
        Returns a list of template names to be used for the request. Must return
        a list. May not be called if render_to_response is overridden.
        """

        template = self.fragment_name if self.request.is_ajax() \
            else self.template_name

        if template is None:
            return super(SingleObjectTemplateResponseMixin) \
                .get_template_names(self)
        else:
            return [template, ]

class OctopusDetailView(AjaxDetailResponseMixin, DetailView):

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

class OctopusListView(AjaxDetailResponseMixin, ListView):

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)
