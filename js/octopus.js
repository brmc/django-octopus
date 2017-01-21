$(function(){
    // Sets the initial state in the browser, so back/forward will
    // work with the landing site
    history.replaceState({
        title: window.location.pathname,
        target: 'body',
        container: $('body').html()
    }, $('title').text(), window.location.pathname);

    /**
     * @param {Event} e
     */
    function prepareLinkRequest(e){
        e.preventDefault();

        var link = this;
        if (link.getAttribute('multi') == "False") {
            $(link).disable();
        }

        var insertionMethod = link.getAttribute('insert');
        var request = new Request(link, insertionMethod, this.href);

        request.submit();
    }

    function prepareFormRequest(e){
        e.preventDefault();
        var form = this;
        var data = $(form).serializeArray();
        var insertionMethod = form.getAttribute('insert');
        var request = new Request(form, insertionMethod, this.action, data);

        request.submit();
    }

    $.fn.extend({
        bindOctopus: function(){
            $(this).find('.octopus-link').unbind('click', prepareLinkRequest).bind('click', prepareLinkRequest);
            $(this).find('.octopus-form').unbind('submit', prepareFormRequest).bind('submit', prepareFormRequest);
            return this;
        },
        disable: function(){
            this.css({'pointer-events': 'none'});
            $(this).unbind('click')
                .removeClass('octopus-link')
                .removeClass('octopus-form');
            return this;
        }
    });

    /**
     *
     * @param {HTMLElement} sourceElement
     * @param {string} insertionMethod
     * @param {string} href
     * @param {Object} requestBody
     */
    function Request(sourceElement, insertionMethod, href, requestBody){
        requestBody = requestBody || {};

        /**
         * @type {string}
         */
        var content;

        /**
         * @type {string}
         */
        var errorContent;

        /**
         *
         * @type {Object}
         */
        var browserState = {};

        /**
         * @type {string}
         */
        var title;

        /**
         * @param {string} newContent
         */
        var buildContent = function(newContent){
            var oldContent = $(sourceElement.target).html();

            title = $(sourceElement).attr('title');

            switch(insertionMethod){
                case "append":
                    content = oldContent + newContent;
                    break;
                case "prepend":
                    content = newContent + oldContent;
                    break;
                case "replace":
                default:
                    content = newContent;
            }

        };

        /**
         * @param {Object} jqXHR
         * @param {string} textStatus
         * @param {string} errorThrown
         */
        var buildErrorContent = function(jqXHR, textStatus, errorThrown){
            title = content = errorContent = jqXHR.status + " " + errorThrown;
        };

        /**
         * @param {string} method
         * @return {boolean}
         */
        function isMethodCsrfSafe(method) {
            return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
        }

        /**
         * @param {string} url
         * @return {boolean}
         */
        function isSameOrigin(url) {
            var host = document.location.host;
            var protocol = document.location.protocol;
            var sr_origin = '//' + host;
            var origin = protocol + sr_origin;

            return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
                (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
                // or any other URL that isn't scheme relative or absolute i.e relative.
                !(/^(\/\/|http:|https:).*/.test(url));
        }

        var insertContent = function(data){
            data = !errorContent ? data : errorContent;

            browserState = {
                title: title,
                target: sourceElement.target,
                container: content
            };

            var elem =  $.parseHTML(data);

            elem = $(elem).addClass("octopus-"+insertionMethod);

            switch(insertionMethod){
                case 'prepend':
                    $(elem).hide();
                    $(sourceElement.target).prepend(elem);

                    $(elem).slideDown("fast", function(){
                        $(sourceElement.target).bindOctopus();
                    });
                    break;
                case 'append':
                    $(elem).hide();
                    $(sourceElement.target).append(elem);

                    $(elem).slideDown("fast", function(){
                        $(sourceElement.target).bindOctopus();
                    });

                    break;
                case 'self':
                    if($(sourceElement).hasClass('octopus-link')){
                        sourceElement = $(sourceElement).parent();
                    }
                    $(sourceElement).fadeOut('fast', function() {
                        this.outerHTML = data;
                        $(this).fadeIn('fast', function(){
                            $('body').bindOctopus();
                        });

                        browserState['target'] = sourceElement;
                    });
                    break;
                default:

                    $(sourceElement.target).fadeOut('fast', function() {
                        $(this).html(elem).fadeIn('fast', function(){
                            $(sourceElement.target).bindOctopus();
                        });
                    });

            }
            if (title != "None" && title != undefined){
                $('title').text(title);

                try{
                    window.history.pushState(browserState, "", href);
                }
                catch(DataCloneError){
                    browserState = {
                        title: 'something went wrong, so we pushed everything',
                        target: 'body',
                        container: $('body').html()
                    };
                    window.history.pushState(browserState, "", href);
                }
            }
        };

        this.submit = function() {
            // Prevent undesirable multiple clicks on a link/element
            if (href == location.href && $(sourceElement).attr('multi') == "False") {
                return;
            }

            var csrftoken = $.cookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!isMethodCsrfSafe(settings.type) && isSameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });


            $.ajax({
                url: href,
                type: $(sourceElement).attr('method'),
                data: requestBody
            }).done(buildContent)
                .fail(buildErrorContent)
                .always(insertContent);
        }
    }


    $('.octopus-link').on('click', prepareLinkRequest);
    $('.octopus-form').on('submit', prepareFormRequest);

    $(window).on('popstate', function(event) {
        var state = event.originalEvent.state;

        if (state) {
            $(state.target).html(state.container );
            $('title').text(state.title);
        }
        $('body').bindOctopus();
    });
});