/* global hljs */

$(document).ready(function () {
    'use strict';

    /**
     * Extend links to external website
     * » add target="_blank"
     * » add rel="noopener noreferer"
     */
    const externalLinks = function () {
        const internalHost = [location.hostname];
        const protocolPattern = /^https?:\/\//i;

        /**
         * Walk through all links on the current page
         */
        $('a').each(function () {
            const href = $(this).attr('href');

            /**
             * Check if it's a http link
             */
            if (protocolPattern.test(href)) {
                const hrefHostname = $(new URL(href)).attr('hostname');

                if ($.inArray(hrefHostname, internalHost) === -1) {
                    $(this).attr('target', '_blank');
                    $(this).attr('rel', 'noopener noreferer');
                }
            }
        });
    };

    /**
     * Render a JS clock for Eve time
     *
     * @param element The HTML element to display the time
     */
    const renderClock = function (element) {
        const date = new Date();

        /**
         * Date
         * @type {string}
         */
        // const year = date.getUTCFullYear();
        // const month = String(date.getUTCMonth() + 1).padStart(2, '0');
        // const day = String(date.getUTCDate()).padStart(2, '0');

        /**
         * Time
         * @type {string}
         */
        const hour = String(date.getUTCHours()).padStart(2, '0');
        const minute = String(date.getUTCMinutes()).padStart(2, '0');
        const second = String(date.getUTCSeconds()).padStart(2, '0');

        element.html(hour + ':' + minute + ':' + second);

        setTimeout(function () {
            renderClock(element);
        }, 500);
    };

    /**
     * Functions that need to be executed on successful ajax events
     */
    $(document).ajaxSuccess(function () {
        externalLinks();
    });

    /**
     * Functions that need to be executed on load
     */
    const init = function () {
        externalLinks();
        renderClock($('.eve-time-wrapper .eve-time-clock'));
        hljs.highlightAll();
    };

    /**
     * Start the show
     */
    init();
});
