[![Build Status](https://travis-ci.org/brmc/django-octopus.svg?branch=master)](https://travis-ci.org/brmc/django-octopus)

# **django-octopus** #

Octopus is a lightweight AJAX pull framework for django, allowing
pages to be loaded or refreshed modularly.

[Click here to see a full-featured demo.](http://mcclure.pw/demo).  The 
demo is still a bit rough around the edges, and has only been tested in Chrome 
and FireFox.  Chrome looks best because there's some wonky problem with the 
menu transitioons on FireFox.  The responsiveness is lazy and violates 
accessibility, and there is no mobile version. But otherwise, it looks and 
works great!! :D

## Contents

* [Quick start](#quick-start)
* [Changelog (Recent changes only)](#changelog-recent-changes)
  * [v0.3.2](#V032)
  * [v0.3.1](#V031)
  * [v0.3](#V03)
  * [v0.2](#V02)
  * [v0.1](#v01)
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
  
You may need to restart your development server to detect the template tags.  

3\. Add javascript:

    <script src="{% static 'octopus/minimum-jquery-2.1.1.js' %}"></script>
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

where `template_name` is the name of a fully rendered template and
`fragment_name` is a stripped down template.  It's recommended to simply
import `fragment_name` into `template_name`.

See [Usage](#views) for more detail information on using generic views or on 
writing your own functional views.

5\. Create your links.  Manually, :

    <a href="{% url 'detail' object.id %}" class="octopus-link"
    target="#container" insert="replace" method="get" title="New title">Link 
    Text</a>

or or with a template tag

    {% a 'Link Text' '#container' 'detail' object.id insert="replace" method="get" title="New title %}

See [Usage](#template-tags) for details on what these parameters mean and other 
parameters and their default values.

6\. Putting it all together, a template might look like [this](#creating-templates)


## Changelog (Recent Changes)

## v0.4

* due to changes in django, new dependencies are required:
    
    'django.contrib.auth',
    'django.contrib.contenttypes'
  
* Added javascript build commands: see `BUILD_INSTRUCTIONS.md` for details
* Includes custom build of jQuery to use only the required components
* Trivial javascript improvements

## v0.3.1

* removed deprecated template tag

## v0.3.1

* officially added support for django 1.8, 1.9, and 1.10 and python 3.5
* removed support for EOL versions of django

## v0.3

### Bug fixes

* fixed bug in the javascript that prevented replaceState() from being called
in FireFox

### Changes

* a `title` is now required to engaged the forward/back behavior

* `multi` default value for forms changed to `True`

* the behavior of `self` was modified to fully replace the containing element,
  so be sure a single node encapsulates your template fragments if using
  `self`


## v0.2.1

## Bug fixes

* Corrected error message from ImproperlyConfigured `tentacles.py` to display 
 the incorrect value
 
* JS files weren't updating the title.  

## v0.2

### Changes

* `action` attribute in the template tags was changed to `insert` to avoid
conflicts with form attributes.  This is NOT backwards compatible.

* The div that wraps elements that were prepended or appended has been removed

* Changed the name of the file in the template tag from `a.py` to
`tentacles.py`. `{% load a %}` is deprecated.  Change it to
`{% load tentacles %}`


### Features

* Create-, Update-, and DeleteViews support added and tested.

* New template tag to create forms

* Added `self` to allowed `insert` methods.  This is similar to `replace` but
in case several nodes have been appended or prepended, it only replaces the
exact node in question rather than overwriting the contents of the entire
`target`.  This allows for creating, editing, or deleting multiple models in
place and saving them individually. If `insert="self"` is set, `target` is
ignored.

* `multi` attribute added to template tags to prevent or allow multiple clicks 
on a link.  
    **Default: False**

* When elements are loaded they are given a class corresponding to their 
insertion method so you can hook into them if you wish.   
**Naming schema** octopus-<insert method>, e.g. `octopus-append`


### v0.1

#### Features

* New generic class-based views that correspond to DetailView, ListView, 
 ArchiveIndexView, DayArchiveView, TodayArchiveView, DateDetailView, 
 WeekArchiveView, MonthArchiveView, and YearArchiveView
 
* A mixin(AjaxResponseMixin) to be used on pre-existing CBVs

* A template tag to generate octopus-compatible links


## Requirements ##

1. Python 2.7, 3.4, 3.5, 3.6

2. Django, v1.10+

3. jQuery 1.11+ (A custom build is provided that only uses the  
minimum required components) 

## How does it work?

Special links are created using a template tag that are intercepted when 
clicked by a simple jQuery script and routed via AJAX to views that are 
defined to conditionally render a full template when one navigates 
directly to a URL(or if javascript is unavailable) or to render a specific 
portion of the template if requested via AJAX(will be made more descriminating 
later).  The HTML returned by the server is then inserted into a node in the 
DOM specified by a link attribute. Browser states are updated to preserve full 
back/forward functionality.

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
components of jQuery. It is built off of v2.1.1.

jQuery should be loaded before `octopus.js`

    <script src="{% static 'octopus/minimum-jquery-2.1.1.js' %}"></script>
    <script src="{% static 'octopus/octopus.js' %}"></script>
   

## Usage ##

There's just three main steps:

1. Create your views

2. Create your links (with or without the template tag)

3. Create your templates

### Views ###

#### Creating Class-Based Views ####

Generic views have been created for the detail, list, time-based, and update 
views following the naming convention of tacking `Octopus` onto existing view 
names: `Octopus<OriginalViewName>`.  If that doesn't make sense, here's 
an explicit list of the available views with their 
respective counter parts:

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

You use these just as you would the normal CBV's.  The only difference is that 
You also need to define a `fragment_name` in addition to the `template_name` 

    from octopus.views import OctopusDetailView
    from yourapp.models import YouModel
    
    class YourDetailView(OctopusDetailView):
        model = YourModel
        template_name = "puzzle.html"
        fragment_name = "puzzlepiece.html"
        
But if you don't feel like defining the fragment names, just like 
`template_suffix`, a `fragment_suffix` of `'_fragment` has been provided.  So 
you can just name your templates accordingly.  But note, the `fragment_suffix` 
is appened **after** the `template_suffix`, so if your full template was called 

    yourapp/yourmodel_detail.html
    
then your fragment template should be called

    yourapp/yourmodel_detail_fragment.html


**If you are using the update views, you should be sure your `success_url` also 
returns a template fragment**


#### Creating Function-Based Views

The only caveat is to wrap your template definition in an `is_ajax()` method:

    def your_vew(request, *args, **kwargs):
        ...
        if request.is_ajax():
            template = "template_fragment.html"
        else:
            template = "full_template.html"
        ...


#### Using the AjaxResponseMixin with existing views ####


You can convert your existing CBV's into OctopusViews like so:

    from octopus.views import AjaxResponseMixin 
    
    class YourView(AjaxResponseMixin, YourCustomBaseView):
        parent = YourCustomBaseView
        template_name = "weeewoo.html"
        fragment_name = "weeedoo_fragment.html"
        ...
        
`parent` is defined so get_template_names() can be called in case something 
 goes wrong.

### Template Tags ###

#### a ####

Only the first three arguments are requried, but in your template, you would 
build a full link like so: 

    {% load tentacles %}
    
    {% a "Link Text" "#container" "detail" object.id method="post" insert="prepend" id="cantelope" classes="inline-block article" title="Manatee killed by Cantelope" %}
    
This would create an anchor with the id `cantelope` and classes `octopus-link`, 
`inline-block, article`. `octopus-link` is added automatically to provide 
the necessary functionality. When clicked, the link would make a request to 
the url/path rendered from the url named `detail` passing it the `object.id` 
via a `POST` request. The HTML returned would then be prepended to `#container`, 
and the document would be give a new title.

**note: to engage the back/forward functionality, be sure to give a title, 
otherwise the browser state will not be updated**

The order for the template tags are: 

Link text, target element, url name, url arguments, kwargs. 

* **Link Text**: the visible, clickable text for the link.
 
* **Target Element**: the html node that will receive the rendered template 
returned from the ajax request. E.g., `main`, `#container`, `.container`

* **URL name**: the name of the url as defined in your urlconfs to be 
passed to reverse(). If settings.OCTOPUS_ALLOW_MANUAL is set to True, you may 
pass a hard-coded url.

* **URL arguments**: as many parameters you wish/need to pass to reverse
 
* **Kwargs**:
    * **method**: the HTTP Method with which you wish to make the ajax request.  
    **Default** `get`
    
    * **insert**: how the incoming text will be inserted  
      **values**: `replace`, `prepend`, `append`, `self`   
      **Default**: `replace`  
      **Note**: `self` is similar to `replace`, but rather than overwriting 
        everything in the entire node, `self` replaces just the object in 
        question.  This is particularly useful for editing forms.
      
    
    * **classes**: a string of class names.  
      **pass the names, rather than the selectors**: i.e., "class1, class2" rather than ".class1, .class2"   
      **Default**: None
    
    * **id**: like above but for the Id.  
      **Default**: None

    * **title**: Text for the `<title>` node.  If a title is not given, then 
        the browser state will not be updated, and forward/ back functionality
        will not be preserved.
      **Default**: None
    
#### form ####

The syntax is similar to the link tag:

    {% load tentacles %}
    
    {% form "Button Text" form_instance request.path method="get" classes="monkeypus" id="create" insert="append" target="footer" title="Milksteak for Champions" %}


A couple things to note.

1. the second argument passed to the form tag is an instance of a form object

2. `target` becomes a kwarg because `insert=self` is more useful for forms and 
  it supercedes anything defined by target. `target` can still be used as long 
  as `insert` is redefined to be anything other than `self`


3. Like "Link Text" above, "Button Text" will be the text on the submit button

4. `request.path` is passed to `url_name`.  You can still pass named urls and 
their arguments to the tag if you want to, but when dealing with the generic 
edit views, if you use `request.path` you won't have to create individual forms 
for each the views.  **make sure you include 
`'django.core.context_processors.request',` in `TEMPLATE_CONTEXT_PROCESSORS`**

The rest of the arguments remain the same.  The only difference are couple of 
the default values:

* **Kwargs**
    * **method**: Default: `post`
    
    * **replace**: Default `self`
    
**Note: the template uses form.as_p() by default**

### Manually Creating Elements

#### Creating Links ####

The template tag only creates standard inline text links. If you want to 
create a link on an image or need some extra data attributes, you will have to 
build the links yourself.

But it's not hard. The only required attributes are:

* `href="..."`

* `target="..."`

* `class="octopus-link ..."`

Then you can pass the kwargs as defined in [Template Tags](#a)

#### Creating Forms ####

If you want to render something besides form.as_p(), you'll have to create your 
own form.  Beside the standard required attributes for forms, the only thing 
unique to octopus is to add a hook for the javascript:
 
    class="octopus-form ..."

This is what the 

Then you can pass the kwargs as defined in [Template Tags](#a)

### Creating templates ###

A simple template schema that uses both links and forms might look something 
like this:

Base template:

    {% load static %}
    {% load tentacles %}
    <!doctype html>
    <html>
    <head>
        <title>Document</title>
    </head>
    <body>
        {% a 'create object' 'main' 'create' %}
        <main>
            {% block content %}
            {% endblock content %}
        </main>
        ...
        <footer>
            <script src="//code.jquery.com/jquery-1.11.2.min.js" type="text/javascript"></script>
            <script src="{% static 'octopus/both.js' %}" type="text/javascript"></script>
        </footer>
    </body>
    </html>
    
model_form.html:

    {% extends "base.html" %}
    {% block content %}
        {% include "model_form_fragment.html" %}
    {% endblock %}

model_form_fragment.html

    {% load tentacles %}
    
    {% form 'Submit' form_instance request.path %}

## Configuration ##

So far there is only one setting:

### OCTOPUS_ALLOW_MANUAL ###

The determines whether hard-coded links may be passed to the template tag

**Default**: `True`

## Todo ##

 * Make data-hooks html5 compliant

 * Create `fragment` template tag so new templates dont necessarily have to be 
 created.

 * Write some tests for AjaxResponseMixin
 
 * Decorator for FBVs
 
 * Make the determining factor the the template stricter so it's more than just 
 AJAX or not
 
 * Allow user more control over prepend, append, and replace behaviors: speed, 
  effects, etc.
  
 * Allow settings to be set per view rather than globally
 
 * Add compatibility with django-media-helper
