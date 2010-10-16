(function($){

    $.fn.clipexpand = function clipexpand() {
        var img = this;
        try {
            img.position();
        } catch (e) {
            window.setTimeout(function(){
                $(img).clipexpand();
            }, 100);
            return null;
        }

        function get_clip() {
            var clip = img.css('clip');
            var values = clip.match(/\d+\.?\d*/g);
            return {
                'top': values[0],
                'right': values[1],
                'bottom': values[2],
                'left': values[3]
            }
        }

        function set_clip(clip) {
            img.css('clip', 'rect('+clip.top+'px, '+clip.right+'px, '+clip.bottom+'px, '+clip.left+'px)');
        }

        function adjust_dimension(dimension) {
            var desired = img.css(dimension).match(/\d+/)[0];
            var clip = get_clip();

            if (dimension == 'height') {
                var original = parseInt(img.attr('data-height'));
                var fixed = desired / ( Math.abs(clip.bottom - clip.top) / original );
                clip.top = clip.top * (fixed / original);
                clip.bottom = clip.bottom * (fixed / original);
            } else {
                var original = parseInt(img.attr('data-width'));
                var fixed = desired / ( Math.abs(clip.right - clip.left) / original );
                clip.left = clip.left * (fixed / original);
                clip.right = clip.right * (fixed / original);
            }

            // Under some conditions, changing width/height changes the other
            var other_original = (dimension == 'width' && img.css('height')) || img.css('width');
            img.css(dimension, fixed);
            (dimension == 'width' && img.css('height', other_original)) || img.css('width', other_original)

            if (dimension == 'height') {
                clip.bottom = parseFloat(clip.top) + parseFloat(desired);
            } else {
                clip.right = parseFloat(clip.left) + parseFloat(desired);
            }
            set_clip(clip);
        }

        adjust_dimension('width');
        adjust_dimension('height');

        var pos = img.position();
        var clip = get_clip();

        pos.top = (pos.top || 0) - clip.top;
        pos.left = (pos.left || 0) - clip.left;
        img.css({
            top: pos.top + 'px',
            left: pos.left + 'px'
        });

        $(this).trigger('clipexpanded');
    };

})(jQuery);
