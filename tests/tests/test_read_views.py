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

    def test_get_context_data(self):
        response = self.client.get('/detail/%d' % self.m.id, {},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        base_template = response.context['base_template']
        self.assertTrue("octopus/ajax.html" == base_template)

        response = self.client.get('/detail/%d' % self.m.id, {})

        base_template = response.context['base_template']
        self.assertTrue("base.html" == base_template)

    def test_fragment_response(self):
        response = self.client.get('/detail/%d' % self.m.id, {},
                                   HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        conversation = response.content.strip()

        self.assertTrue(
            conversation.startswith('Fancy people talking about fancy dances'))

        self.assertTrue('The truth' not in conversation)
        self.assertTrue(
            conversation.endswith('Loneliness, violence, and peanut butter'))

    def test_full_response(self):
        response = self.client.get('/list/', {}).content.strip()

        self.assertTrue('too much milksteak' in response)
