This package is ahead of pypi so the instructions no longer apply  
to versions installed with package managers.

[![Build Status](https://travis-ci.org/brmc/django-octopus.svg?branch=master)](https://travis-ci.org/brmc/django-octopus)

# **django-octopus** #

Octopus is a lightweight AJAX pull framework for django that uses a  
purely declarative syntax to load or refresh pages modularly.

[Click here to see a full-featured demo.](http://mcclure.pw/demo).   
The content of the demo hasn't been updated to match the changes with  
version 0.4.  It behaves the same from the end-user perspective,  
but the information is no longer accurate

## Contents

* [Quick start](#quick-start)
* [Changelog (Recent changes only)](#changelog-recent-changes)
* [How does it work?](#how-does-it-work)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
    * [Views](#views)
        * [Creating Class Based Views](#creating-class-based-views)
        * [Creating function Based Views](#creating-function-based-views)
    * [Template Tags](#template-tags)
        * [a (links)](#a)
        * [form](#form)
    * [Manually Creating Elements](#manually-creating-elements)
        * [Creating Links](#creating-links)
        * [Creating forms](#creating-forms)
    * [Creating Templates](#creating-templates)
* [Configuration](#configuration)
* [Todo](#todo)


## Quick start ##

1\. `pip install django-octopus`

2\. `settings.py`

    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        ...
        'octopus',
        ...
    )
  
You may need to restart your development server to detect the template  
tags.  

3\. Add javascript:

    <script src="{% static 'octopus/custom-jquery.js' %}"></script>
    <script src="{% static 'octopus/octopus.js' %}"></script>

4\. Define your views:

    from octopus.views import OctopusDetailView, OctopusListView

    def YourDetailView(OctopusDetailView):
        model = YourModel
        template_name = "<template name>"
        base_template = '<some base template>'

    def YourListView(OctopusListView):
        model = YourModel
        template_name = "<template name>"
        base_template = '<some base template>'

where `template_name` extends `base_template` 

See [Usage](#views) for more detail information on using generic views  
or on writing your own functional views.

5a\. When extending a template, use the context variable `base_template`  
instead of a string literal:

Do this:

    {% extends base_template %}
    
Not this:

    {% extends 'base.html' %}

5b\. In the same template, create a {% block fragment %} and optionally  
 a {% block title %}
 
    {% block title %}<title>Detail View </title>{% endblock fragment %}
    {% block fragment %}<div> some content </div>{% endblock fragment %}

6\. In another template, link to the first template.  

Manually:

    <a href="{% url 'detail' object.id %}" 
       class="octopus-link"
       data-oc-target="#container" 
       >Link Text</a>

or with a template tag:

    {% a 'detail' object.id target='#container' text='Link Text' %}

Where `#container` is the selector of a DOM element that already  
exists in your template  

See [Usage](#template-tags) for details on what these parameters mean  
and other parameters and their default values.


7\. Putting it all together, a template might look like  
[this](#creating-templates)


## Changelog (Recent Changes)

## v0.4

This is an aggressive update that breaks backwards compatibility in  
just about every way, but seeing that no one really uses it, the fallout  
should be minimal :)

### New features

* Proxy templates are no longer used to switch between full and ajax  
requests. You now just define blocks named `fragment` in your 
templates.
* Titles are included directly in the response.  Before, titles were  
defined on the link itself. Now a `title` block is supported to define  
title content
* While loading, the target element fades to 30% opacity

### Changes 

* removed support for python < 3.6
* due to changes in django, new installed apps are required: 
   
   INSTALLED_APPS = (
        ...
        'django.contrib.auth',
        'django.contrib.contenttypes'
        ...
   )
    
* changed the template tags' signatures to resemble the typical order of  
html tag attributes:  

    \<a href='/home' data-oc-target="#main">text\</text>

    {% a '/home' target='#main' text='text' %}
    
* Changed default value for `multi` to `True`
* Switched to using data-* html attributes
  
### Javascript changes

* Added javascript build commands: see `BUILD_INSTRUCTIONS.md` for details
* Includes custom build of jQuery to use only the required components
*Trivial javascript improvements, still needs a lot of work before a  
1.0 release. Jasmine tests are still missing


## Requirements ##

1. Python 3.6+

2. Django, v1.8+

3. jQuery 1.11+ (A custom build is provided that only uses the  
minimum required components) 

## Installation ##

1\. Install Octopus: 

    pip install django-octopus
    
2\. Add to INSTALLED_APPS:

    settings.py
    
    INSTALLED_APPS = (
        'django.contrib.auth',
        'django.contrib.contenttypes',
        ...
        'octopus'
    )
    
A `RunTimeError` will be thrown if auth and contenttypes are not loaded
    
3\. Include the javascript to your templates.

jQuery is required. If you're not using it already, a custom build is  
provided that only uses the `css`, `ajax`, `events`, and `effects`  
components of jQuery.

If you're new to this, jQuery should be loaded before `octopus.js`

    <script src="{% static 'octopus/custom-jquery.js' %}"></script>
    <script src="{% static 'octopus/octopus.js' %}"></script>

## How does it work?

In the client, you create links or forms with various  
data-attributes to determine how content should be handled  
once it is retrieved from the server. All behavior is defined  
declaratively meaning it's not necessary to write any javascript.  

When a user navigates directly to a url, the page is rendered in full  
like expected, but when a link is clicked or a form submitted, it is  
intercepted and routed to the server via ajax where your django  
app then returns only the content of your template defined in a   
`{% block fragment %}`

The response is then inserted into the target node(s) defined on the  
clicked element. Browser states are updated to preserve full  
back/forward functionality.  


## Usage ##

There's three main steps:

1. Create your view

2. Create your link or form

3. Create your template(s)

### Views ###

#### Creating Class-Based Views ####

Generic views have been created for the following class-based views:

| Octopus View            |      Django View |
|-------------------------|------------------|
| OctopusTemplateView     | TemplateView     |
| OctopusDetailView       | DetailView       |
| OctopusListView         | ListView         |
| OctopusArchiveIndexView | ArchiveIndexView |
| OctopusDayArchiveView   | DayArchiveView   |
| OctopusTodayArchiveView | TodayArchiveView |
| OctopusDateDetailView   | DateDetailView   |
| OctopusWeekArchiveView  | WeekArchiveView  |
| OctopusMonthArchiveView | MonthArchiveView |
| OctopusYearArchiveView  | YearArchiveView  |
| OctopusCreateView       | CreateView       |
| OctopusUpdateView       | UpdateView       |
| OctopusDeleteView       | DeleteView       |
| OctopusFormView         | FormView         |

You use these as you would normal CBV's.  The only additional requirement  
is that you need to define `base_template` in addition to `template_name` 

    from octopus.views import OctopusDetailView
    from yourapp.models import YouModel
    
    class YourDetailView(OctopusDetailView):
        model = YourModel
        base_template = "base.html"
        template_name = "template.html"
        
`base_template` will be sent as a context variable and should be used  
in the `extends` tag instead of the string literal. More on that later.  


**If you are using the update views, you should be sure your 
`success_url` also returns a template fragment**

#### Creating Function-Based Views

The only caveat is to wrap your template definition in an `is_ajax()` method:

    def your_vew(request, *args, **kwargs):
        ...
        if request.is_ajax():
            base_template = "octopus/ajax.html"
        else:
            base_template = "base.html"
        ...
        
        context['base_template'] = base_template

`octopus/ajax.html` is a real template and should be included exactly as  
written above

#### Using the AjaxResponseMixin with existing views ####

You can convert your existing CBV's into OctopusViews like so:

    from octopus.views import AjaxResponseMixin 
    
    class YourView(AjaxResponseMixin, YourCustomBaseView):
        base_name = "weeedoo.html"
        template_name = "weeewoo.html"
        
        
### Template Tags ###

Be sure to load the `tentacles` tags

    {% load tentacles %}    

#### a ####

Here is the method signature of the tag: 

    a(href: str,
      *href_args,
      text: str,
      target: str,
      insert: str='replace',
      method: str='get',
      multi: bool=True,
      **kwargs) -> dict:


* **href**: the name of the url as defined in your urlconfs or a  
hard-coded url

* **href_args**: parameters will be passed to  `django.urls.resolvers.reverse`

* **text**: the visible, clickable text of the link.
 
* **target**: the selector of the html node(s) that will receive the  
server response. E.g., `main`, `#container`, `.container`
 
* **method**: the HTTP Method to use when making the request.  
    **default** `get`

* **insert**: how the incoming text will be inserted into the document  
  **values**: `replace`, `prepend`, `append`, `self`   
  **default**: `replace`  
  **note**: `self` is similar to `replace`, but rather than overwriting 
    everything in the entire node, `self` replaces just the object in 
    question.  This is particularly useful for editing forms.
* **multi**: whether a link may be click multiple times
    **default**: True
* **kwargs**: arbitrary parameters will be converted to html attributes  

Here is a minimal example:  

    {% load tentacles %}

    {% a '/home' target='#main' text='click me' %}

Here is a full example
    
    {% a "detail" object.id target="#container" text="Link Text" method="post" insert="prepend" id="cantelope" class="inline-block article" data-some-random-attr='1' %}
    
    
#### form ####

The syntax for a form is similar to the link tag:

    {% load tentacles %}
    
    {% form request.path form=form_instance text="Button Text" %}

A couple things to note.

1. a form instance is must be passed

2. `target` becomes optional because the default insertion method  
`insert=self` is more useful for forms and supercedes anything  
defined by target. `target` can still be used as long as `insert` is  
redefined to be anything other than `self`

4. `request.path` is passed to `url_name`.  You can still pass named urls and   
their arguments to the tag if you want to, but when dealing with the generic  
edit views, if you use `request.path` you won't have to create individual forms   
for each view.  
**make sure you include 
`'django.core.context_processors.request',` in `TEMPLATE_CONTEXT_PROCESSORS`**

The rest of the arguments remain the same.  The only difference are couple of  
the default values:

* **Kwargs**
    * **method**: Default: `post`
    
    * **replace**: Default `self`
    
**Note: the template uses form.as_p()**

### Manually Creating Elements

#### Creating Links ####

The template tags  create standard html tags. If you want to 
create a link on an image or need some extra data attributes, you will have to 
build the links yourself.

But it's not hard. Non-standard attributes (target, method, multi) are  
 prefixed with `data-oc-`

The only requirements are:

* `href="..."`

* `data-oc-target="..."`

* `class="octopus-link ..."`

Then you can set anything defined in [Template Tags](#a)

#### Creating Forms ####

If you want to render something besides form.as_p(), you'll have to create your 
own form.  Beside the standard required attributes for forms, the only thing 
unique to octopus is to add a hook for the javascript:
 
    class="octopus-form ..."
    
and in adition to setting `method=` you need to set `data-oc-method=`

Then you can set anything defined in [Template Tags](#a)

### Creating templates ###

A simple template schema that uses both links and forms might look something 
like this:

base_template = 'base.html':

    {% load static %}
    {% load tentacles %}
    <!doctype html>
    <html>
    <head>
        {% block title %}
        <title>Document</title>
        {% endblock title %}
    </head>
    <body>
        {% a 'create' text='create object' target='main' %}
        <main>
            {% block fragment %}
            {% endblock fragment %}
        </main>
        ...
        <footer>
            <script src="{% static 'octopus/custom-jquery.js' %}" type="text/javascript"></script>
            <script src="{% static 'octopus/both.js' %}" type="text/javascript"></script>
        </footer>
    </body>
    </html>
    
model_form.html:

    {% extends base_template %}
    {% load tentacles %}
    
    {% block fragment %}        
        {% form request.path text='Submit' form=form_instance %}
    {% endblock %}

## Configuration ##

So far there is only one setting:

### OCTOPUS_ALLOW_MANUAL ###

The determines whether hard-coded links may be passed to the template tag

**Default**: `True`

## Todo ##
 
 * Allow user more control over prepend, append, and replace behaviors: speed, 
  effects, etc.
  
 * Allow settings to be set per view rather than globally