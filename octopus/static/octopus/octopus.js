$(function(){
    // Sets the initial state in the browser, so back/forward will
    // work with the landing site
    history.replaceState({
        title: window.location.pathname,
        target: 'body',
        container: $('body').html()
    }, $('title').text(), window.location.pathname);

    function link_helper(e){
        if ($(this).attr('multi') == "False")
            $(this).disable();

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
            $(this).find('.octopus-link').unbind('click', link_helper).bind('click', link_helper);
            $(this).find('.octopus-form').unbind('submit', form_helper).bind('submit', form_helper);
            return this;
        },
        disable: function(){
            this.css({'pointer-events': 'none'});
            return this;
        }
    });

    function request(obj, insert, href, dataArray){
        // Prevent undesirable multiple clicks on a link/element
        if (href == location.href && $(obj).attr('multi') == "False")
            return;

        var content = new String;

        var error_content;  // container for error messages
        var state = {};     // Dict to pass to pushState
        dataArray = dataArray || {};

        $.ajax({
            url: href,
            type: $(obj).attr('method'),
            data: dataArray
        }).done(function(data){
            title = $(obj).attr('title');

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

            var elem = $.parseHTML(data);
            elem = $(elem).addClass("octopus-"+insert);
            switch(insert){
                case 'prepend':
                    $(elem).hide();
                    $(obj.target).prepend(elem);

                    $(elem).slideDown("fast", function(){
                        $(obj.target).bindOctopus();
                    });
                    break;
                case 'append':
                    $(elem).hide();
                    $(obj.target).append(elem);

                    $(elem).slideDown("fast", function(){
                        $(obj.target).bindOctopus();
                    });

                    break;
                case 'self':
                    if($(obj).hasClass('octopus-link')){
                            obj = $(obj).parent();
                    }
                    $(obj).fadeOut('fast', function() {
                        this.outerHTML = data;
                        $(this).fadeIn('fast', function(){
                            $('body').bindOctopus();
                        });

                        state['target'] = obj;
                    });
                    break;
                default:

                    $(obj.target).fadeOut('fast', function() {
                        $(this).html(elem).fadeIn('fast', function(){
                            $(obj.target).bindOctopus();
                        });
                    });

            }
            if (title != "None" && title != undefined){
                $('title').text(title);

                try{
                    window.history.pushState(state, "", href);
                }
                catch(DataCloneError){
                    state = {
                        title: 'something went wrong, so we pushed everything',
                        target: 'body',
                        container: $('body').html()
                    };
                    window.history.pushState(state, "", href);
                }
            }


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
        $('body').bindOctopus();
    });
});