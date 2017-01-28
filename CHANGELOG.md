# Changelog

## v0.4

* due to changes in django, new dependencies are required:

    'django.contrib.auth',
    'django.contrib.contenttypes'

* Added javascript build commands: see `BUILD_INSTRUCTIONS.md` for details
* Includes custom build of jQuery to use only the required components
* While loading, the target element fades to 30%
* Trivial javascript improvements
* Titles are included directly in the response.  Before, titles were  
defined on the link itself. Now a `title` block is supported to define  
  title content

## v0.3.2

* removed deprecated 'a' tag

## v0.3.1

* officially added support for django 1.8, 1.9, and 1.10 and python 3.5.
* removed support for EOL versions

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

## v0.2

### Changes

* `action` attribute in the template tags was changed to `insert` to avoid
conflicts with form attributes.  This is not backwards compatible.

* Changed the name of the file in the template tag from `a.py` to
`tentacles.py`. `{% load a %}` is deprecated.  Change it to
`{% load tentacles %}`


### New Features

* Create-, Update-, and DeleteViews support added and tested.

* New template tag to create forms

* Added `self` to allowed `insert` methods.  This is similar to `replace` but
in case several nodes have been appended or prepended, it only replaces the
exact node in question rather than overwriting the contents of the entire
`target`.  This allows for creating, editing, or deleting multiple models in
place and saving them individually. If `insert="self"` is set, `target` is
ignored.

## v0.1

### Features

* New generic class-based views that correspond to DetailView, ListView,
 ArchiveIndexView, DayArchiveView, TodayArchiveView, DateDetailView,
 WeekArchiveView, MonthArchiveView, and YearArchiveView

* A mixin(AjaxResponseMixin) to be used on pre-existing CBVs

* A template tag to generate octopus-compatible links