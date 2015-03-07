from collections import OrderedDict
from django.template.loader import render_to_string
from django.test import TestCase, RequestFactory, Client
from octopus.templatetags.a import a
from test_app.models import TestModel


class TagsTest(TestCase):
    def setUp(self):
        self.m = TestModel()
        self.m.save()
        self.id = self.m.id

    def test_a_single_arg(self):
        self.assertEqual(
            a(
                "text",
                "target",
                "detail",
                self.id,
                action="append",
                classes="poop",
                id="man",
                title="title"),
            OrderedDict({
                'id': 'man',
                'target': 'target',
                'action': 'append',
                'method': 'get',
                'classes': 'poop',
                'href': '/detail/1',
                'title': 'title',
                'text': 'text'
            })
        )

    def test_a_multi_arg(self):
        self.assertEqual(
            a(
                "text",
                "target",

                "multi",
                self.id,
                'a',
                action="prepend",
                method='get',
                classes="poop",
                id="man",
                title="title"),
            OrderedDict({
                'id': 'man',
                'target': 'target',
                'action': 'prepend',
                'classes': 'poop',
                'method': 'get',
                'href': '/multi/1/a',
                'title': 'title',
                'text': 'text'
            })
        )
    def test_a_no_arg(self):
        self.assertEqual(
            a(
                "text",
                "target",
                "list",
                method='post',
                classes="poop",
                id="man",
                title="title"),
            OrderedDict({
                'id': 'man',
                'target': 'target',
                'action': 'replace',
                'method':'post',
                'classes': 'poop',
                'href': '/list/',
                'title': "title",
                'text':'text'
            })
        )

    def test_render_template(self):
        context = a(
            "text",
            "target",
            "detail",
            self.id,
            action="append",
            classes="poop",
            id="man",
            title="title"
        )

        self.assertEqual(render_to_string('octopus/link.html', context),
            u'<a id="man" target="target" action="append" method="get" class="octopus-link poop" href="/detail/%d" title="title">text</a>' % self.id
        )

    def test_render_template_nokwargs(self):
        context = a(
            "text",
            "target",
            "detail",
            self.id,
            action="prepend",
         )

        self.assertEqual(render_to_string('octopus/link.html', context),
            u'<a target="target" action="prepend" method="get" class="octopus-link" href="/detail/%d" title="None">text</a>' % self.id
        )