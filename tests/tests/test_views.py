from datetime import date
from django.test import TestCase, RequestFactory, Client
from test_app.models import TestModel


class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.m = TestModel()
        self.m.date = date(2015, 2, 21)
        self.id = self.m.save()
        self.n = TestModel()
        self.n.date = date.today()
        self.n.save()

    def test_ajax_DetailView(self):

        response = self.client.get('/detail/%d' % self.m.id,  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(b"fragment", response.content)

    def test_full_DetailView(self):
        response = self.client.get('/detail/%d' % self.m.id)

        self.assertEqual(b"full", response.content)

    def test_ajax_ListView(self):
        response = self.client.get(
            '/list/',
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual(b"list fragment", response.content)

    def test_full_ListView(self):
        response = self.client.get('/list/')

        self.assertTrue(b"full" in response.content)

    def test_ajax_SuffixView(self):
        response = self.client.get('/suffix/%d' % self.m.id,  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(b"suffix", response.content)

    def test_ajax_OctopusArchiveIndexView(self):
        response = self.client.get('%s' % 'archive',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(b"archive", response.content)

    def test_ajax_OctopusDateDetailView(self):
        response = self.client.get('/2015/feb/21/%d/' % self.m.id,  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(b"suffix", response.content)


    def test_ajax_OctopusYearArchiveView(self):
        response = self.client.get('/2015/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(
            [u'test_app/testmodel_archive_year_fragment.html'],
            response.template_name)


    def test_ajax_OctopusArchiveIndexView(self):
        response = self.client.get('/archive/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(
            [u'test_app/testmodel_archive_fragment.html'],
            response.template_name)

    def test_ajax_OctopusDayArchiveView(self):
        response = self.client.get('/2015/feb/21/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(
            [u'test_app/testmodel_archive_day_fragment.html'],
            response.template_name)

    def test_ajax_OctopusWeekArchiveView(self):
        response = self.client.get('/2015/week/07/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(
            [u'test_app/testmodel_archive_week_fragment.html'],
            response.template_name)

    def test_ajax_OctopusMonthArchiveView(self):
        response = self.client.get('/2015/feb/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
        self.assertEqual(
            [u'test_app/testmodel_archive_month_fragment.html'],
            response.template_name)

    def test_ajax_OctopusTodayArchiveView(self):
       response = self.client.get('/today/',  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest", follow=True)
       self.assertEqual(
           [u'test_app/testmodel_archive_day_fragment.html'],
           response.template_name)
