#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from django import template
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from octopus import settings

register = template.Library()


def create_html_tag(text, target, href, *href_args, **kwargs):
    """
    builds a link that can be used by static/octopus.js.


    Arguments:
    :param text: This varies depending on the calling function.  See below for
        more details.
    :type text: str
    :param target: The html element, class, or id to catch the returned data
    :type target: str with the selector prefix if applicable: body, .className,
        #idname
    :param insert: Dictates how to handle the incoming data. Allowed values:
        replace, append, prepend.
        Defaults to replace
    :type insert: str
    :param href: The name of the url pattern defined in your urls.py
    :type href: str
    :param href_args: Any arguments to be passed to this url
    :param kwargs: Expected kwargs(with default in parentheses):
        method("get"), insert("replace"), classes(None), id(None), title(None)
    :type kwargs: str
    :return: OrderedDict
    """

    try:
        href = reverse(href, args=href_args)
    except NoReverseMatch:
        if settings.ALLOW_MANUAL is True:
            href = href
        else:
            raise NoReverseMatch

    # I'm setting default values here rather than above so that the tag would
    # be easier to use and feel more natural.
    method, insert, multi, classes, id_ = \
        map(kwargs.get,
            ['method', 'insert', 'multi', 'class', 'id'],
            ['get',    'replace', False,   '',      ''])

    if insert.lower() not in ['replace', 'append', 'prepend', 'self']:
        raise ImproperlyConfigured("%s is not a valid value for insert. It "
                                   "should be: replace, append, prepend, or self."
                                    % insert)

    return OrderedDict(
        (('id', id_),
        ('target', target),
        ('insert', insert),
        ('class', classes),
        ('method', method),
        ('href', href),
        ('text', text),
        ('multi', multi)))


@register.inclusion_tag('octopus/link.html')
def a(text, target, url_name, *url_args, **kwargs):
    """ Wrapper to create a link compatible with Octopus

    :param text: The clickable text of the link
    :type text: str
    :returns: dict
    """

    return create_html_tag(text, target, url_name, *url_args, **kwargs)


@register.inclusion_tag('octopus/form.html')
def form(text, form, url_name, *url_args, **kwargs):
    """ Wrapper to create a form compatible with Octopus

    :param form: an instance of a form
    :type form: FormObject
    :param text: The text that goes on the Submit button
    :type text: str
    :returns: dict
    """

    # Default values for forms should differ from regular links
    kwargs['method'], kwargs['insert'], kwargs['multi'] = \
        map(kwargs.get, ['method', 'insert', 'multi'],
                        ['post',   'self',   'True'])

    context = create_html_tag(text, kwargs.pop('target', None),
                              url_name, *url_args, **kwargs)
    context['form'] = form

    return context
