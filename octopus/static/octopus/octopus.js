$(function(){
    // Sets the initial state in the browser, so back/forward will
    // work with the landing site
    history.replaceState({
        title: window.location.pathname,
        target: 'body',
        container: $('body').html()
    });

    function request(title, obj, error_content, action, d){
        $.ajax({
            url: obj.href,
            type: $(obj).attr('method'),
            data: d
        }).done(function(data){
            title = obj.title;

            switch(action){
                case "append":
                    content = $(obj.target).html() + data;
                    break;
                case "prepend":
                    content = data + $(obj.target).html();
                    break;
                case "replace":
                    content = data;
            }

        }).fail(function( jqXHR, textStatus, errorThrown){
            title = content = error_content = jqXHR.status+" "+errorThrown;
        }).always(function(data){
            data = !error_content ? data : error_content;

            var state = {
                title: title,
                target: obj.target,
                container: content
            };

            switch(action){
                case 'prepend':
                    var elem = $(document.createElement('div')).html(data).hide();
                    $(obj.target).prepend(data);
                    $(elem).slideDown();
                    break;
                case 'append':
                    var elem = $(document.createElement('div')).html(data).hide();
                    $(obj.target).append(elem);
                    $(elem).slideDown();
                    break;
                default:
                    $(obj.target).fadeOut('fast', function() {
                        $(this).html(data).fadeIn('slow');
                        $('title').text(title);
                    });
            }
            window.history.pushState(state, "", obj.href);
        });
    }

    $(.octopus).on('submit', function(e){
        e.preventDefault();

    });

    $('.octopus-link').click(function(e){
        e.preventDefault();

        var title = new String;  var content = new String;
        var obj = this;
        var error_content;  // container for error messages
        var state = {};     // Dict to pass to pushState
        var action = $(obj).attr('action');
        var d = this.serializeArray();
        request(title, obj, error_content, action, d);

    });

    $(window).on('popstate', function(event) {
        var state = event.originalEvent.state;

        if (state) {
            $(state.target).html(state.container );
            $('title').text(state.title);
        }
    });
});