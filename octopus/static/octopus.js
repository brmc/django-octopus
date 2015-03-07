$(function(){
    history.replaceState({
        title: window.location.pathname,
        target: 'body',
        container: $('body').html()
    });


    $('a.octopus-link').click(function(e){
        e.preventDefault();

        var obj = this;
        var type = this.type == "" ? 'get' : this.type;
        var title = content = "";
        var state = {};

        var request = $.ajax({
            url: this.href,
            type: type
        }).done(function(data){

            title = obj.title;
            switch(obj.action)
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
            state = {
                title: title,
                target: obj.target,
                container: data
            };

        }).fail(function( jqXHR, textStatus, errorThrown){
            title = content = jqXHR.status+" "+errorThrown;
            state = {
                title: title,
                target: obj.target,
                container: content
            };
        }).always(function(){
            $(obj.target).fadeOut('fast', function() {
                $(this).html(content).fadeIn('slow');
                $('title').text(title);
                window.history.pushState(state, "", obj.href);
            });
        });
    });

    $(window).on('popstate', function(event) {
        var state = event.originalEvent.state;

        if (state) {
            $(state.target).html(state.container );
            $('title').text(state.title);
        }
    });
});