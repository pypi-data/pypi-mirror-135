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
     * Add leading zero if number is below 10
     *
     * @param {string} i
     * @returns {string}
     */
    const addLeadingZero = function (i) {
        if (i < 10) {
            i = '0' + i;
        }

        return i;
    };

    /**
     * Render a JS clock for Eve time
     *
     * @param element
     * @param {int} utcOffset
     */
    const renderClock = function (element, utcOffset) {
        const today = new Date();
        let h = today.getUTCHours();
        let m = today.getUTCMinutes();
        let s = today.getUTCSeconds();

        h = h + utcOffset;

        if (h > 24) {
            h = h - 24;
        }

        if (h < 0) {
            h = h + 24;
        }

        h = addLeadingZero(h);
        m = addLeadingZero(m);
        s = addLeadingZero(s);

        element.html(h + ':' + m + ':' + s);

        setTimeout(function () {
            renderClock(element, 0);
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
        renderClock($('.eve-time-wrapper .eve-time-clock'), 0);
        hljs.highlightAll();
    };

    /**
     * Start the show
     */
    init();
});
