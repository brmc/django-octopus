# coding: utf-8
import django
if django.VERSION >= (1, 7):

    from django.apps import AppConfig

    class TestAppConfig(AppConfig):
        name = 'test_app'
