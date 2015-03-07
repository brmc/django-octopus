#!/usr/bin/env python
# -*- coding: utf-8 -*-
from collections import OrderedDict
from django import template
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from octopus import settings

register = template.Library()


@register.inclusion_tag('octopus/link.html')
def a(text, target, url_name, *url_args, **kwargs):
    """
    builds a link that can be used by static/octopus.js.


    Arguments:
    :param text: The link text: </a>Text</a>
    :type text: str
    :param target: The html element, class, or id to catch the returned data
    :type target: str with the selector prefix if applicable: body, .className,
        #idname
    :param action: Dictates how to handle the incoming data. Allowed values:
        replace, append, prepend.
        Defaults to replace
    :type action: str
    :param url_name: The name of the url pattern defined in your urls.py
    :type url_name: str
    :param url_args: Any arguments to be passed to this url
    :param kwargs: Expected kwargs(with default in parentheses):
        method("get"), action("replace"), classes(None), id(None), title(None)
    :type kwargs: str
    :return: OrderedDict
    """

    try:
        href = reverse(url_name, args=url_args)
    except NoReverseMatch:
        if settings.ALLOW_MANUAL is True:
            href = url_name
        else:
            raise NoReverseMatch

    # I'm setting default values here rather than above so that the tag would
    # be easier to use and feel more natural.
    method, action, classes, id_, title = \
        map(kwargs.get, ['method', 'action', 'classes', 'id', 'title'],
                        ['get',    'replace', None,     None,  None, ])

    if action.lower() not in ['replace', 'append', 'prepend']:
        raise ImproperlyConfigured("%s is not a valid value for action. It "
                                   "should be: replace, append, or prepend.")

    return OrderedDict({
        'id': id_,
        'target': target,
        'action': action,
        'classes': classes,
        'method': method,
        'href': href,
        'title': title,
        'text': text
    })
