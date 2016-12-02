from datetime import date
from django.test import RequestFactory
from django.test.testcases import TestCase
from ..test_app.models import TestModel


class TestEditViews(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.m = TestModel()
        self.m.date = date(2015, 2, 21)
        self.id = self.m.save()
        self.n = TestModel()
        self.n.date = date.today()
        self.n.save()

    def test_create_view(self):
        response = self.client.get('/create/', {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(["test_app/testmodel_form_fragment.html", ],
                         response.template_name)

    def test_create_view_success(self):
        response = self.client.post('/create/',
            { 'date': date(2015, 2, 21) },
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(200, response.status_code)
        self.assertTrue('fragment_list.html' in response.template_name)

    def test_create_view_failure(self):
        response = self.client.post('/create/',
            {'date': 1},
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertTrue('test_app/testmodel_form_fragment.html' in response.template_name)

    def test_update_view(self):
        response = self.client.get('/update/1',
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(["test_app/testmodel_form_fragment.html", ],
                         response.template_name)

    def test_update_success(self):
        response = self.client.post('/update/1',
            { 'date': date(2015, 2, 21) },
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual(200, response.status_code)
        self.assertTrue('fragment_list.html' in response.template_name)

    def test_update_view_failure(self):
        response = self.client.post('/update/1',
            {'date': 1},
            follow=True,
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")

        self.assertTrue('test_app/testmodel_form_fragment.html' in response.template_name)

    def test_delete_view(self):
        response = self.client.get('/delete/1',
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest")
        self.assertEqual("test_app/testmodel_confirm_delete_fragment" in
                         response.template_name)

    def test_delete_view(self):
        response = self.client.post('/delete/1',
            {},
            HTTP_X_REQUESTED_WITH="XMLHttpRequest",
            follow=True)
        self.assertTrue("fragment_list.html" in
                         response.template_name)

