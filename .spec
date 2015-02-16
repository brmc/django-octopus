This should be a simple ajax pull framework to modularly load a website as
the navigation is traversed.

Views will be defined to conditionally render
either a full template or a fragment of a template.
Both functional and
    check decorator possibilities
    it should work more or less like:
      if request.is_ajax()
        swap out template for fragment

class-based views can be used. New generic views will be provided.
    add property of fragment_name to be used
    override the post method.
     if ajax, return fragment_name instead of template_name



 When
defining links, give the link a "target" attribute along with an action.  The
action being one of the following: append, prepend, overwrite.  You can either
manually create these or use the template tag/filter
{% a 'urlname' 'arguments' 'action' 'id' 'classes' %}

    needs render to template


ajax:
    needs unique class name for links
    stop propagation

    if link was already called, load data from
    post link

    on success,
        load html.
        replace, append, or prepend html to target.
        copy to dummy zone.
        change URL bar
        push/pop state