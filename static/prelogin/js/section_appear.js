$(function () {
    'use strict';

    var $sections = $('.section.appear');
    $sections.appear();

    var getNextSection = function ($elem, depth) {
        if ($elem.next().hasClass('appear')) {
            return $elem.next();
        }
        if (depth >= 5) {
            return false;
        }
        depth ++;
        return getNextSection($elem.next(), depth);
    };

    var removeNext = function ($elem) {
        if ($elem.find('.container .next-nav').length >= 1) {
            $elem.find('.container .next-nav').fadeOut(600, function () {
                $(this).remove();
            });
        }
    };

    var addNext = function ($appender) {
        if ($appender.find('.container .next-nav').length < 1) {
            var $nextSection = getNextSection($appender, 0);
            var $nextNav = $('<a class="next-nav" style="display: none;"/>');
            var navId = '.section-lead';
            if ($nextSection) {
                navId = '#' + $nextSection.attr('id');
            }
            $nextNav.attr('href', navId);

            if ($appender.hasClass('appear-last')) {
                $nextNav.html($('<i class="fa fa-angle-double-up" />'));
                $nextNav.addClass('next-nav-last');
            } else {
                $nextNav.html($('<i class="fa fa-angle-double-down" />'));
            }
            $nextNav.data('appender', '#' + $appender.attr('id'));

            $nextNav.click(function (e) {
                e.preventDefault();
                var oldAppender = $(this).data('appender');
                $.scrollTo($($(this).attr('href')), 1000, {
                    offset: {
                        top: -55,
                    },
                    onAfter: function (t, s) {
                        removeNext($(oldAppender));
                    },
                });
            });

            $appender.find('.container').append($nextNav);
            $appender.find('.container .next-nav').fadeIn(600);
        }
    };

    var loadFirst = function () {
        var $first = $($sections[0]);
        addNext($first);
    };

    loadFirst();

    $(document.body).on('appear', '.section.appear', function(e, $affected) {
        // this code is executed for each appeared element
        addNext($affected);
    });
    $(document.body).on('disappear', '.section.appear', function(e, $affected) {
        // this code is executed for each appeared element
        removeNext($affected);
    });
});
