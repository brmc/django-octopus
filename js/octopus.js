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
            $(this).off('click', '.octopus-link', prepareLinkRequest)
                .on('click', '.octopus-link', prepareLinkRequest);
            $(this).off('submit', '.octopus-form',  prepareFormRequest)
                .on('submit', '.octopus-form', prepareFormRequest);
            return this;
        },
        disable: function(){
            this.css({'pointer-events': 'none'});
            $(this).off('click', 'octopus-link').removeClass('octopus-link')
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
        var parseResponseIntoTitleAndContent = function(newContent){
            var oldContent = $(sourceElement.target).html();

            title = $(newContent).filter('title').text().trim();

            newContent = $(newContent).not('title');

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

        /**
         * @param {string} name
         * @return {string|null}
         */
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = jQuery.trim(cookies[i]);
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }

        var bindOctopusToTarget = function(){
            $(sourceElement.target).bindOctopus();
        };

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
                case 'append':
                    $(elem).hide();
                    $(sourceElement.target)[insertionMethod](elem);
                    $(elem).slideDown("fast", bindOctopusToTarget);
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

            if (title != "" && title !== undefined){
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

            $(sourceElement.target).fadeTo(100, 1);
        };

        this.submit = function() {
            // Prevent undesirable multiple clicks on a link/element
            if (href == location.href && $(sourceElement).attr('multi') == "False") {
                return;
            }

            var csrftoken = getCookie('csrftoken');

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!isMethodCsrfSafe(settings.type) && isSameOrigin(settings.url)) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            });

            $(sourceElement.target).fadeTo(100, .2);

            $.ajax({
                url: href,
                type: $(sourceElement).attr('method'),
                data: requestBody
            }).done(parseResponseIntoTitleAndContent)
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