(function($){

    defaults = {
        cancel: "#user_select_form_cancel",
        save: "#user_select_form_save",
        tagform: "#user_select_form"
    }

    $.fn.photoTagger = function (id, options) {
        if (typeof(options) == "undefined") { options = {}; };
        // For some reason IE barfs if the variable is called 'photo'
        photo_ = $(this);

        photo_.imgAreaSelect({
            enable: true,
            onSelectChange: showuserselect,
            x1: 0, y1: 0, x2: 100, y2: 100
        });

        $(options.cancel).click(function(){
            photo_.imgAreaSelect({ hide: true, disable: true });
            $(options.tagform).hide();
            return false;
        });
        $(options.save).click(function(){
            photo_.imgAreaSelect({ hide: true, disable: true });
            $(options.tagform).hide();
	        $(tagform).ajaxSubmit({success:
                function(){
                    photo_.photoTags(id, {tagsurl: options.tagsurl});
                }});
            return false;
        });
    };

    $.fn.photoTags = function (photo_id, options) {
        var photo = $(this);
        $.getJSON(options.tagsurl(photo_id), function(photo_tags){
            photo.imgNotes(photo_tags);
            populate_tagged_listing(photo_tags);
        });
    };

    function populate_tagged_listing(photo_tags) {
        $('#user_tag_listing_target').empty();
        $.each(photo_tags, function(photo_tag){
            var username = this.username;
            $('#user_tag_listing').show();
            var target = $('#user_tag_listing_target');
            if ( target.text() ) {
                target.append(', ');
            }
            target.append('<a href="/profiles/'+username+'/">'+username+'</a>');
        });
    }

    function showuserselect (image, area) {
        var imageOffset = $(image).offset();
        var form_left = imageOffset.left + parseInt(area.x1);
        var form_top = imageOffset.top + parseInt(area.y2) + 5;

        $('#user_select_form').css({ left: form_left + 'px', top: form_top + 'px'});

        $('#user_select_form').show();

        $('#user_select_form').css('z-index', 10000);

        $('#id_x').val(area.x1);
        $('#id_y').val(area.y1);
        $('#id_height').val(area.height);
        $('#id_width').val(area.width);
    };

    $.widget('ui.photoSelectAndTag', {
        _init: function() {
            var widget = this;
            var element = this.element;
            
            this.img = element.parent().find('img');
            widget.updateImage(element.val());
            element.change(function(){
                var photo_id = element.val();
                widget.updateImage(photo_id);
            });

            this.button = element.parent().find('[name=pb_toggle]');
            this.button.click(function(){
                var jcrop = element.parent().find('.jcrop-holder');
                jcrop.toggle();
            });
            function show_or_hide() {
                if (element.val() == "") {
                    element.parent().find('img').hide();
                    element.parent().find('.jcrop-holder').hide();

                    element.parent().find('[type=hidden]').val('');
                } else {
                    element.parent().find('img').show();
                    element.parent().find('.jcrop-holder').show();
                }
            }
            show_or_hide();
            element.parent().find('select').change(show_or_hide);

            widget.setupAspects() 
        },
        setupAspects: function setupAspects() {
            var widget = this;

            if (widget.options.read_aspect_h && widget.options.read_aspect_w) {
                var aspect_width;
                var aspect_height;

                var updateAspects = function(){ return widget.updateAspects() };
                
                $(widget.options.read_aspect_h).change(updateAspects);
                $(widget.options.read_aspect_w).change(updateAspects);
            }

        },
        updateAspects: function updateAspects() {
            var widget = this;

            aspect_height = $(widget.options.read_aspect_h).val();
            aspect_width = $(widget.options.read_aspect_w).val();
            if (typeof widget.jcrop_api != 'undefined') {
                var force_aspect = aspect_width / aspect_height;
                if (force_aspect != widget.options.force_aspect && !isNaN(force_aspect)) {
                    widget.options.force_aspect = force_aspect; 
                    widget.jcrop_api.setOptions(widget.options);
                    widget.updateImage(widget.photo_id)
                }
            }
        },
        updateBox: function(area) {
            var widget = this;
            var element = this.element;
            widget.area = area;

            data = {x: area.x, y: area.y, width: area.w, height: area.h};
            if (typeof widget.box_id != 'undefined') {
                data['id'] = widget.box_id;
            }
            $.post(
                this.options.ajaxAddPhotoBoxURL.replace('${photo_id}', widget.photo_id.toString()),
                data,
                function(data) {
                    widget.box_id = data;
                    element.parent().find('[type=hidden]').val(data);
                }
            );
        },
        updateImage: function(photo_id) {
            var widget = this;
            var element = this.element;
            if (typeof widget.img != 'undefined') {
                var visible = (widget.img.parent().find('.jcrop-holder').filter(':visible').length == 1);
            } else {
                var visible = false;
            }

            widget.changing = (widget.photo_id != photo_id);
            if (typeof widget.jcrop_api != 'undefined') {
                element.parent().find('.jcrop-holder').remove();
                element.parent().find('img').after('<img class="phototagger_image" src="" />');
                element.parent().find('img:first').remove();
                widget.img = element.parent().find('img');
                delete widget.jcrop_api;
            }

            $.ajax({
                url: this.options.ajaxGetImageURL.replace('${photo_id}', photo_id),
                success: function(data) {
                    widget.photo_id = photo_id
                    widget.img.attr('src', data);
                    function setupJCrop() {
                        var default_width = 100;
                        var default_height = 100;
                        if (widget.options.force_aspect) {
                            default_height = default_width * widget.options.force_aspect;
                        }

                        function update_widget(c) {
                            widget.updateBox(c);
                        };

                        var jcrop_options = {
                            allowMove: true,
                            onSelect: update_widget,
                            setSelect: [widget.options.box.x,
                                        widget.options.box.y,
                                        widget.options.box.x + widget.options.box.width,
                                        widget.options.box.y + widget.options.box.height]
                        };
                        // Setup aspect ratio options
                        if (widget.options.force_aspect) {
                            $.extend(jcrop_options, {
                                aspectRatio: widget.options.force_aspect
                            });
                        }
                        
                        widget.jcrop_api = $.Jcrop(widget.img, jcrop_options);

                        var prev_changing = widget.changing;
                        widget.changing = true;
                        widget.updateAspects();
                        widget.changing = prev_changing;

                        if (!visible && !widget.changing) {
                            setTimeout(function(){
                                widget.img.parent().find('.jcrop-holder').hide()
                            }, 500);
                        }
                    };

                    if (widget.img[0].complete) {
                        setupJCrop();
                    } else {
                        widget.img.load(setupJCrop);
                    }
                }
            });
        }
    });

    $.fn.fitClippedImage = function fitClippedImage() {
        var img = this;
        try {
            img.position();
        } catch (e) {
            window.setTimeout(function(){
                $(img).fitClippedImage();
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
                clip.bottom = parseInt(clip.top) + parseInt(desired);
            } else {
                clip.right = parseInt(clip.left) + parseInt(desired);
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
