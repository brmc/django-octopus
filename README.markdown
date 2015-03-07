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
You may need to 
3\. Templates
    <script src="//code.jquery.com/jquery-1.11.2.min.js" type="text/javascript">
    </script>
    <script src="{% static 'both.js' %}" type="text/javascript"></script>

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

See [Usage](#usage) if you want to define your own views or use functional
views

5\. Create your links.  Manually, :

    <a href="{% url 'detail' object.id %}" class="octopus-link"
    target="#container" action="replace">

or or with a template tag

   {% a 'detail' object.id '#container' 'replace' %}

The order for the template tags are: url name, id or slug, target element to
catch the response, action(replace, append, prepend), then two optional
parameters: a CSS ID name and CSS class names.  Write the selectors
just like you would write them in the HTML tag: "class1, class2" rather than
".class1, .class2"



## Changelog (Recent Changes)

### v0.1

## Requirements ##

jQuery

## How does it work?

Views are defined to conditionally render a full template or

## Usage ##



## Configuration ##

## What it does **not** do (...yet?) ##
