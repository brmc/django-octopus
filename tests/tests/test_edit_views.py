from datetime import date
from django.test import RequestFactory
from django.test.testcases import TestCase
from tests.test_app.models import TestModel


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
        pass

    def test_create_view_failure(self):
        pass

    def test_update_view(self):
        pass

    def test_update_view_failure(self):
        pass

    def test_delete_view(self):
        pass

    def test_delete_view(self):
        pass

