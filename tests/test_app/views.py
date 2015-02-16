from octopus.views import OctopusDetailView, OctopusListView
from test_app.models import TestModel


class DetailView(OctopusDetailView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    model = TestModel
    template_name = "full.html"
    fragment_name = "fragment.html"

class ListView(OctopusListView):
    http_method_names = ['get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace']
    model = TestModel
    template_name = "full.html"
    fragment_name = "fragment.html"

