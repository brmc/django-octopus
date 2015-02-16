from django.conf import settings
from django.conf.urls import patterns, url
from test_app.views import DetailView, ListView


urlpatterns = patterns(
   '',
   url(r'^list/', ListView.as_view(), name="list"),
   url(r'^detail/(?P<pk>\d)', DetailView.as_view(), name="detail"),
)
