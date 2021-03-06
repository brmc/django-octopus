import re
from django.forms.models import ModelForm
from django.template.loader import render_to_string
from django.test import TestCase
from octopus.templatetags.tentacles import a
from test_app.models import TestModel
from octopus.templatetags.tentacles import form


def remove_whitespace(rendered):
    return re.sub('\s{2,}', ' ', rendered)

TestCase.maxDiff = None

class TestA(TestCase):
    def setUp(self):
        self.m = TestModel()
        self.m.save()
        self.id = self.m.id

    def test_a_single_arg(self):
        kwargs = {
            'insert': "append",
            'class': "poop",
            'id': "man"
        }
        expected = {
            'target': 'target',
            'insert': 'append',
            'class': 'poop',
            'method': 'get',
            'href': '/detail/1',
            'text': 'text',
            'multi': True,
            'extra_params': ' id="man"'
        }

        actual = a("detail", self.id, text="text", target="target", **kwargs)

        self.assertEqual(actual, expected)

    def test_a_multi_arg(self):
        kwargs = {
            'insert': "prepend",
            'method': 'get',
            'class': "poop",
        }

        expected = {
            'target': 'target',
            'insert': 'prepend',
            'class': 'poop',
            'method': 'get',
            'href': '/multi/1/a',
            'text': 'text',
            'multi': True,
        }

        actual = a("multi", self.id, 'a', text='text', target='target', **kwargs)

        self.assertEqual(actual, expected)

    def test_a_no_arg(self):
        kwargs = {
            'method': 'post',
            'class': "poop",
            'id': "man"
        }

        actual = a("list", text="text", target="target", **kwargs)
        expected = {
            'target': 'target',
            'insert': 'replace',
            'class': 'poop',
            'method': 'post',
            'href': '/list/',
            'text': 'text',
            'multi': True,
            'extra_params': ' id="man"'
        }

        self.assertEqual(actual, expected)

    def test_render_template(self):
        kwargs = {
            'insert': "append",
            'class': "poop",
            'id': "man"
        }

        context = a(
            "detail",
            self.id,
            text="text",
            target="target",
            **kwargs)

        rendered = render_to_string('octopus/link.html', context)
        actual = remove_whitespace(rendered)

        raw = '<a ' \
              'data-oc-target="target" ' \
              'data-oc-insert="append" ' \
              'data-oc-method="get" ' \
              'class="octopus-link poop" ' \
              'href="/detail/{:d}" ' \
              'data-oc-multi="True" ' \
              'id="man">text</a>'
        expected = raw.format(self.id)

        self.assertEqual(actual, expected)

    def test_render_template_no_kwargs(self):
        context = a(
            "detail",
            self.id,
            text="text",
            target="target",
            insert="prepend")

        rendered = render_to_string('octopus/link.html', context)
        actual = remove_whitespace(rendered)

        expected = '<a ' \
                   'data-oc-target="target" ' \
                   'data-oc-insert="prepend" ' \
                   'data-oc-method="get" ' \
                   'class="octopus-link" ' \
                   'href="/detail/{:d}" ' \
                   'data-oc-multi="True">text</a>'.format(self.id)

        self.assertEqual(actual, expected)


class TestForm(TestCase):
    class MForm(ModelForm):
        class Meta:
            model = TestModel
            fields = ('date',)

    def test_render_minimum_form(self):
        self.maxDiff = None
        context = form(
            "/",
            text="submit",
            form=self.MForm)

        actual = render_to_string('octopus/form.html', context)
        actual = remove_whitespace(actual)

        expected = render_to_string('test_app/form.html', {'form': self.MForm})
        expected = remove_whitespace(expected)

        self.assertEqual(actual, expected)

    def test_render_full_form(self):
        kwargs = {
            'method': "get",
            'insert': "append",
            'target': "#main",
            'id': "id",
            'class': "class"
        }

        context = form(
            "/",
            text="submit",
            form=self.MForm,
            **kwargs)

        actual = render_to_string('octopus/form.html', context)
        actual = remove_whitespace(actual)

        expected = render_to_string(
            'test_app/full_form.html', {'form': self.MForm})
        expected = remove_whitespace(expected)

        self.assertEqual(actual, expected)
