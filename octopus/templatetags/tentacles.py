#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.forms import Form, BaseForm
from django.template.smartif import key

from octopus import settings

register = template.Library()


def create_context(href: str,
                   *href_args,
                   text: str,
                   target: str,
                   insert: str='replace',
                   method: str='get',
                   multi: bool=True,
                   **kwargs) -> dict:
    """

    :param href: a url name or a raw url
    :param href_args: optional arguments to be passed to
    django.core.urlresolvers.reverse
    :param text: the clickable text
    :param target: a dom id where the response will be injected
    :param insert: how the content will be injected. Possible values:
    replace, append, prepend, self
    :param method: HTTP method
    :param multi: whether a link may be clicked multiple times
    :param kwargs: any kwarg will be forwarded to the template in the format:
        `key1="val" key2="val2"`
    """

    try:
        href = reverse(href, args=href_args)
    except NoReverseMatch:
        if settings.ALLOW_MANUAL is not True:
            raise NoReverseMatch

        href = href


    if insert.lower() not in ['replace', 'append', 'prepend', 'self']:
        error_message = u"'{}' is not a valid value for insert. It " \
                        u"should be: replace, append, prepend, " \
                        u"or self.".format(insert)

        raise ImproperlyConfigured(error_message)

    class_ = kwargs.pop('class', '')

    context = {
        'target': target,
        'insert': insert,
        'class': class_,
        'method': method,
        'href': href,
        'text': text,
        'multi': multi,
    }

    params = [f' {key}="{val}"' for key, val in kwargs.items()]

    if params:
        context['extra_params'] = ' '.join(params)

    return context

@register.inclusion_tag('octopus/link.html')
def a(*args, **kwargs) -> dict:
    """ Wrapper to create a link compatible with Octopus

    :returns: dict: context object
    """

    return create_context(*args, **kwargs)


@register.inclusion_tag('octopus/form.html')
def form(href: str,
         *href_args,
         form: BaseForm,
         text: str,
         target: str=None,
         insert: str='self',
         method: str='post',
         **kwargs) -> dict:
    """
    :param href: a url name or raw url set on the action property of a form
    :param href_args: optional parameters to be passed to href
    :param form: an instance of a form object
    :param text: displayed on the submit button
    :param target: a dom id where the response will be injected
    :param insert: how the content will be injected. Possible values:
    replace, append, prepend, self
    :param method: HTTP method
    :param kwargs:
    :return:
    """

    context = create_context(
        href, *href_args, text=text, target=target, insert=insert, method=method, **kwargs)

    context['form'] = form

    return context
