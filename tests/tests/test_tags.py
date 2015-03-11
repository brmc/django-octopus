from collections import OrderedDict
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.test import TestCase
from octopus.templatetags.tentacles import a
from test_app.models import TestModel
from tests.octopus.templatetags.tentacles import form


class TestA(TestCase):
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
                insert="append",
                classes="poop",
                id="man",
                title="title"),
            OrderedDict({
                'id': 'man',
                'target': 'target',
                'insert': 'append',
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
                insert="prepend",
                method='get',
                classes="poop",
                id="man",
                title="title"),
            OrderedDict({
                'id': 'man',
                'target': 'target',
                'insert': 'prepend',
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
                'insert': 'replace',
                'method': 'post',
                'classes': 'poop',
                'href': '/list/',
                'title': "title",
                'text': 'text'
            })
        )

    def test_render_template(self):
        context = a(
            "text",
            "target",
            "detail",
            self.id,
            insert="append",
            classes="poop",
            id="man",
            title="title"
        )

        self.assertEqual(
            render_to_string('octopus/link.html', context),
            u'<a id="man" target="target" insert="append" method="get" '\
            'class="octopus-link poop" href="/detail/%d" '\
            'title="title">text</a>' % self.id
        )

    def test_render_template_nokwargs(self):
        context = a(
            "text",
            "target",
            "detail",
            self.id,
            insert="prepend",
        )

        self.assertEqual(
            render_to_string('octopus/link.html', context),
            u'<a target="target" insert="prepend" method="get" ' \
            'class="octopus-link" href="/detail/%d" title="None">text</a>'
            % self.id)


class TestForm(TestCase):

    class MForm(ModelForm):
        class Meta:
            model = TestModel
            fields = ('date', )

    def test_render_minimum_form(self):
        context = form(
            "submit",
            self.MForm,
            "/"

        )
        self.assertEqual(
            render_to_string('octopus/form.html', context),
            render_to_string('test_app/form.html', {'form': self.MForm}),)

    def test_render_full_form(self):

        context = form(
            "submit",
            self.MForm,
            "/",
            method="get",
            insert="append",
            target="#main",
            id="id",
            classes="class"
        )
        self.assertEqual(render_to_string('octopus/form.html', context),
                         render_to_string(
                             'test_app/full_form.html', {'form': self.MForm}),)
