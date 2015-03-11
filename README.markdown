# **django-octopus** #

Octopus is a lightweight AJAX pull framework for django, allowing
pages to be loaded or refreshed modularly.

## Contents

* [Quick start](#quick-start)
* [Changelog (Recent changes only)](#changelog-recent-changes)
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
        ...
        'octopus',
        ...
    )
    
You may need to restart your development server to detect the template tags.  

3\. Add javascript:

    <script src="//code.jquery.com/jquery-1.11.2.min.js" type="text/javascript">
    </script>
    <script src="{% static 'octopus/both.js' %}" type="text/javascript"></script>

4\. Define your views:

    from octopus.views import OctopusDetailView, OctopusListView

    def YourDetailView(OctopusDetailView):
        model = YourModel
        template_name = "<template name>"
        fragment_name = "<template fragment name>"

    def YourListView(OctopusListView):
        model = YourModel
        template_name = "<template name>"
        fragment_name = "<template fragment name>"

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

## v0.2

### Changes

* `action` attribute in the template tags was changed to `insert` to avoid
conflicts with form attributes.  This is NOT backwards compatible.

### v0.1

#### Features

* New generic class-based views that correspond to DetailView, ListView, 
 ArchiveIndexView, DayArchiveView, TodayArchiveView, DateDetailView, 
 WeekArchiveView, MonthArchiveView, and YearArchiveView
 
* A mixin(AjaxResponseMixin) to be used on pre-existing CBVs

* A template tag to generate octopus-compatible links

## Requirements ##

1. Python 2.7, 3.3, or 3.4

2. Django, v1.5+

3. jQuery (Tested with 1.11 but probably works with any recent version that 
 supports deferred.done, deferred.fail, and deferred.always methods)

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

1\. install octopus:

    pip install django-octopus
    
2\. Add to INSTALLED_APPS:

    settings.py
    
    INSTALLED_APPS = (
        ...
        'octopus'
    )
    
3\. Include the appropriate javascript to your templates, depending on the 
  following scenarios:

  A.  Make sure you have jQuery included before the `octopus` JS files.  If 
  you're lazy, here's a quick link for you:
  
    <script src="//code.jquery.com/jquery-1.11.2.min.js" type="text/javascript"></script>

  B.  If you need CSRF protection(i.e., for a POST request), include `ajax.js`

    <script src="{% static 'octopus/ajax.js' %}" type="text/javascript"></script>
    
  This is just the JS pulled directly from djangoproject.com:    
  https://docs.djangoproject.com/en/dev/ref/csrf/#ajax  
  so feel free to write your own.  There's nothing special about it.
  
  C.  Include `octopus.js`
  
    <script src="{% static 'octopus/octopus.js' %}" type="text/javascript"></script>
    

  D.  If you need both, you can skip B and C and just include `both.js`
  
    <script src="{% static 'octopus/both.js' %}" type="text/javascript"></script>
    

## Usage ##

There's just two steps:

1. Create your views

2. Create your links (with or without the template tag)

### Views ###

#### Creating Class-Based Views ####

Generic views have been created for the detail, list, time-based, and update 
views following the naming convention of tacking `Octopus` onto existing view 
names: `Octopus<OriginalViewName>`.  If that doesn't make sense, here's 
an explicit list of the available views with their 
respective counter parts:

| Octopus View            |      Django View |
|-------------------------|------------------|
| OctopusView             | View             |
| OctopusTemplateView     | TemplateView
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

    * **title**: Text for the `<title>` node.  
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

 * Write some tests for AjaxResponseMixin
 
 * Decorator for FBVs
 
 * Make the determining factor the the template stricter so it's more than just 
 AJAX or not
 
 * Allow user more control over prepend, append, and replace behaviors: speed, 
  effects, etc.
  
 * Allow settings to be set per view rather than globally
 
 * Add compatibility with django-media-helper
