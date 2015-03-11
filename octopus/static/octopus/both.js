$(function() {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    var csrftoken = getCookie('csrftoken');

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });
  // Sets the initial state in the browser, so back/forward will
    // work with the landing site
    history.replaceState({
        title: window.location.pathname,
        target: 'body',
        container: $('body').html()
    });

    function link_helper(e){
       e.preventDefault();
        var insert = $(this).attr('insert');
        request(this, insert, this.href);
    }

    function form_helper(e){
       e.preventDefault();
        var data = $(this).serializeArray();
        request(this, $(this).attr('insert'), this.action, data);
    }

    $.fn.extend({
        bindOctopus: function(){
            $(this).find('.octopus-link').unbind('click').bind('click', link_helper);
            $(this).find('.octopus-form').unbind('submit').bind('submit', form_helper);

        }
    });

    function request(obj, insert, href, dataArray){

        var title = new String;  var content = new String;
        var error_content;  // container for error messages
        var state = {};     // Dict to pass to pushState

        dataArray = dataArray || {};

        $.ajax({
            url: href,
            type: $(obj).attr('method'),
            data: dataArray
        }).done(function(data){
            title = obj.title;

            switch(insert){
                case "append":
                    content = $(obj.target).html() + data;
                    break;
                case "prepend":
                    content = data + $(obj.target).html();
                    break;
                case "replace":
                default:
                    content = data;
            }

        }).fail(function( jqXHR, textStatus, errorThrown){
            title = content = error_content = jqXHR.status+" "+errorThrown;
        }).always(function(data){
            data = !error_content ? data : error_content;

            state = {
                title: title,
                target: obj.target,
                container: content
            };

            switch(insert){
                case 'prepend':
                    var elem = $(document.createElement('div')).html(data).hide();
                    $(obj.target).prepend(elem);
                    $(elem).slideDown("fast", function(){
                        $(obj.target).bindOctopus();
                    });
                    break;
                case 'append':
                    var elem = $(document.createElement('div')).html(data).hide();
                    $(obj.target).append(elem);
                    $(elem).slideDown("fast", function(){
                        $(obj.target).bindOctopus();
                    });

                    break;
                case 'self':
                    $(obj).fadeOut('fast', function() {
                        $(obj).html(data).fadeIn('fast', function(){
                            $(obj.target).bindOctopus();
                        });
                        $('title').text(title);
                    });
                    break;
                default:

                    $(obj.target).fadeOut('fast', function() {
                        $(this).html(data).fadeIn('fast', function(){
                            $(obj.target).bindOctopus();
                        });
                        $('title').text(title);
                    });
            }
            window.history.pushState(state, "", href);

        });
    }


    $('.octopus-link').on('click', link_helper);
    $('.octopus-form').on('submit', form_helper);

    $(window).on('popstate', function(event) {
        var state = event.originalEvent.state;

        if (state) {
            $(state.target).html(state.container );
            $('title').text(state.title);
        }
    });
});