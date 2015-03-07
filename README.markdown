**edit:  I guess I should point out that this repo doesn't do anything yet.  I started with the readme and tests, so yea, if you're expecting to get anywhere with the QuickStart, then you're going to be a bit disappointed. sorry.**

# **django-octopus** #

Octopus is/will be a lightweight AJAX pull framework for django, allowing
pages to be loaded or refreshed modularly.

## Contents

* [Quick start](#quick-start)
* [Changelog (Recent changes only)](#changelog-recent-changes)
  * [v0.1](#v01)
* [How does it work?](#how-does-it-work)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
* [Configuration](#configuration)
* [What it does not do (...yet?)](#what-it-does-not-do-yet)


## Quick start ##

1\. `pip install git+git://github.com/brmc/django-octopus.git`

2\. `settings.py`

    INSTALLED_APPS = (
        ...
        'octopus',
        ...
   )
You may need to restart your development server to detect the template tags.  

3\. Templates
    <script src="//code.jquery.com/jquery-1.11.2.min.js" type="text/javascript">
    </script>
    <script src="{% static 'octopus.js' %}" type="text/javascript"></script>

4\. Define your views:

    from octopus.views import OctopusDetailView, OctopusListView

    def YourDetailView(OctopusDetailView):
        model = YourModel
        template_name = "template name"
        fragment_name = "fragment name"

    def YourListView(OctopusListView):
        model = YourModel
        template_name = "template name"
        fragment_name = "fragment name"

where `template_name` is the name of a fully rendered template and
`fragment_name` is a stripped down template.  It's recommended to simply
import `fragment_name` into `template_name`.

See [Usage](#views) for more detail information on using generic views or on  
writing your own functional views.

5\. Create your links.  Manually, :

    <a href="{% url 'detail' object.id %}" class="octopus-link"
    target="#container" action="replace" method="get" title="New title">Link 
    Text</a>

or or with a template tag

   {% a 'Link Text' '#container' 'detail' object.id action="replace" method="get" title="New title %}


See [Usage](#template-tags) for details on optional and default parameters.

## Changelog (Recent Changes)

### v0.1

## Requirements ##

jQuery

## How does it work?

Views are defined to conditionally render a full template or

## Usage ##

### Views ###

### Template Tags ###

The order for the template tags are: 

Link text, target element, url name, url arguments, kwargs.

* **Link Text**: the visible, clickable text for the link.
 
* **Target Element**: the html node that will receive the rendered template 
returned from the ajax request. E.g., `main`, `#container`, `.container`

* **URL name**: the name of the url as defined in your urlconfs to be 
passed to reverse().  If settings.OCTOPUS_ALLOW_MANUAL is set to True, you may 
pass a hard-coded url.

* **URL arguments** are as many parameters you wish/need to pass to reverse
 
* **Kwargs**:
    * **method**: the HTTP Method with which you wish to make the ajax request. 
    **Default** `get`
    
    * **action**: `replace`, `prepend`, `append`  
    **Default** `replace`
    
    * **classes**: a string of class names.  **pass the names, rather than the 
    selectors**: i.e., "class1, class2" rather than ".class1, .class2" 
    **Default**: None
    
    * **id**: like above but for the Id.
    **Default**: None

    * **title**: Text for the <title> node.
    **Default**: None
 
### Manually Create your Links

The template tag only creates standard inline text links.  If you want to  
create a link on an image or need some extra data attributes, you will have to 
build the links yourself.

But it's not hard. The only required attributes are:

* href="..."

* target="..."

* class="octopus-link ..."

Then you can pass the kwargs as defined in [Template Tags](#template-tags)


## Configuration ##

## What it does **not** do (...yet?) ##
