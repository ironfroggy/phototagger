(function($){

    defaults = {
	cancel: "#user_select_form_cancel",
	save: "#user_select_form_save",
	tagform: "#user_select_form",
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
            if (widget.options.box.id) {
                widget.box_id = widget.options.box.id;
            }

            this.img = element.next('img');
            widget.updateImage(element.val());
            element.change(function(){
                var photo_id = element.val();
                widget.updateImage(photo_id);
            });
        },
        updateBox: function(area) {
            var widget = this;
            console.log("creating box", widget.photo_id);

            data = {x: area.x1, y: area.y1, width: area.width, height: area.height};
            if (typeof widget.box_id != 'undefined') {
                data['id'] = widget.box_id;
            }
            $.post(
                this.options.ajaxAddPhotoBoxURL.replace('${photo_id}', widget.photo_id.toString()),
                data,
                function(data) {
                    widget.box_id = data;
                    console.log("Created new box", data);
                }
            );
        },
        updateImage: function(photo_id) {
            var widget = this;
            var element = this.element;

            $.ajax({
                url: this.options.ajaxGetImageURL + photo_id,
                success: function(data) {
                    widget.photo_id = photo_id
                    widget.img.attr('src', data);
                    var imgarea_options = {
                        enable: true,
                        x1: widget.options.box.x || 0,
                        y1: widget.options.box.y || 0,
                        x2: widget.options.box.x + widget.options.box.width || 100,
                        y2: widget.options.box.y + widget.options.box.height || 100,
                        onSelectChange: function(i,a){widget.updateBox(a);}
                    };
                    console.log(widget.options.box);
                    console.log(imgarea_options);
                    widget.img.imgAreaSelect(imgarea_options);
                }
            });
        }
    });

})(jQuery);
