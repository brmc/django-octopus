from django.test import TestCase, RequestFactory, Client
from django.core.urlresolvers import reverse
from test_app.models import TestModel


class ViewsTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()

    def test_ajax_DetailView(self):
        m = TestModel()
        m.save()

        response = self.client.post('/detail/%d' % m.id,  {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual("fragment", response.content)

    def test_full_DetailView(self):
        m = TestModel()
        m.save()
        m = TestModel.objects.first()
        response = self.client.get('/detail/%d' % m.id)

        self.assertEqual("full", response.content)

    def test_ajax_ListView(self):
        response = self.client.post(
            '/list/',
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertEqual("fragment", response.content)

    def test_full_ListView(self):
        response = self.factory.post(
            reverse('list', ))

        c = Client()
        response = self.client.get('/list/')

        self.assertTrue("full" in response.content)
