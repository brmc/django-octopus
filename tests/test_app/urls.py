from django import VERSION


from django.conf.urls import url
from django.views.generic.base import TemplateView
from .views import DetailView, ListView, SuffixView, \
    DateDetailView, YearArchiveView, \
    ArchiveIndexView, DayArchiveView, WeekArchiveView, MonthArchiveView, \
    TodayArchiveView,UpdateView, CreateView, DeleteView

url_list = [
    url(r'^/?$', TemplateView.as_view(template_name='base.html'), name="home"),
    url(r'^create/$', CreateView.as_view(), name="create"),
    url(r'^update/(?P<pk>\d)$', UpdateView.as_view(), name="update"),
    url(r'delete/(?P<pk>\d)$', DeleteView.as_view(), name='delete'),
    url(r'^list/', ListView.as_view(), name="list"),
    url(r'^detail/(?P<pk>\d)', DetailView.as_view(), name="detail"),
    url(r'^suffix/(?P<pk>\d)', SuffixView.as_view(), name="suffix"),
    url(r'^multi/(?P<pk>\d)/(?P<s>\w)', DetailView.as_view(), name="multi"),
    url(r'^(?P<year>\d{4})/week/(?P<week>\d+)/$', WeekArchiveView.as_view(),
        name='week'),
    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/(?P<day>\d+)/$',
        DayArchiveView.as_view(), name='day'),
    url(r'^(?P<year>\d+)/(?P<month>[-\w]+)/(?P<day>\d+)/(?P<pk>\d+)/$',
        DateDetailView.as_view(), name="date"),
    url(r'^archive/$', ArchiveIndexView.as_view(), name="archive"),
    url(r'^(?P<year>\d{4})/$', YearArchiveView.as_view(), name='year'),

    url(r'^(?P<year>\d{4})/(?P<month>[-\w]+)/$', MonthArchiveView.as_view(),
        name='month'),
    url(r'^today/$', TodayArchiveView.as_view(), name='today'),
]

if VERSION >= (1,10):
    urlpatterns = url_list
else:
    from django.conf.urls import patterns
    urlpatterns = patterns(
        '',
        *url_list
    )

