PhotoTagger
===========

Intro
-----

This application provides two related features. The first feature is designed
to tag users in photos. The second is to crop photos for display in controlled
layouts. These will probably be split into two applications soon.

Photo Cropping In-place
-----------------------

There are times when we want to clip an image on the browser, but we also need to specify the placement and size of the resulting photo. The CSS clip property only hides what is outside the clip, but the whole image still takes up its space.

The jquery.clipexpand.js plugin, included as part of this project, takes the clip property of the image and expands that region to fill the entire space the image layout uses.

For example:

    ---------------
    |             |
    | whole image |
    |             |
    |      -------|
    |      |      |
    |      | clip |
    ---------------

In this example, the region named "clip" will be moved up and right the entire image resized so that the visible clipped region fills the entire space in the layout the original image would have taken, before the clip.

Using it is as simple as calling clipexpand() on the image element:

    $('.clipexpand').clipexpand();

Photo Cropping
--------------

The idea behind the cropping feature is that you have a collection of images,
in our case from the photos app from Pinax, and in other models you have fields
that need to be filled by not only selecting a photo, but also selecting a
cropped portion of the area. Further, you may want to define those models such
that the photo fields restrict the ratio of the region of the photo.


    from django.db import models
    from phototagger.fields import PhotoBoxField

    class BlogPost(models.Model):
        title = models.CharField(max_length=100)
        body = models.TextField()
        thumbnail = PhotoBoxField(force_aspect=(1, 1), related_name='_blogpost_thumbnail')


In this example we defined a very basic blog post model, which has a title, text
body, and allows the user to select a photo from the available collection and
crop a 1x1 ratio region to use as a thumbnail.

Later, in a template where we want to display the post, we can use that field to generate
the `<img>` tag directly.

    <div class=post>
        {{ post.thumbnail }}
        <h1>{{ post.title }}</h1>
        <div class=post-body>
            {{ post.body }}
        </div>
    </div>

A simple javascript library is provided that does the cropping on the client-side. This is done for two reasons:

1) To add animation effects later, such as multiple crop regions to pan between.

2) To allow multiple regions selected as different ratios, and only load one image to keep in the browser cache. For example, a thumbnail field and a full_image field, so you have a preview in the listing and see the full image otherwise, but only load the image once.
