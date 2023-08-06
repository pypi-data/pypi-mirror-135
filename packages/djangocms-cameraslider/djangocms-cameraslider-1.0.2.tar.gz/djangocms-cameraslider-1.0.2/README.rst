djangocms-cameraslider
=====================
This is a simple `django-cms`_ plugin that implements the jQuery Camera Slider/Slideshow library. 

Dependencies
------------
- django>=3.2
- django-cms>=3.9

Installation
------------
To install::

    pip install djangocms-cameraslider

Then add djangocms-cameraslider to your installed apps::

    INSTALLED_APPS = [
        ...
        'djangocms_cameraslider',
        ...
    ]

If you're not already using `django-filer`_, `easy-thumbnails`_ and `djangocms-text-ckeditor`_ then these too will need to be added to your installed apps::

    INSTALLED_APPS = [
        ...
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        ...
    ]


And run the migrations::

    ./manage.py migrate

The package assume that jQuery has been added to the site already. So if you're not using already, please add to you templates/base.html:

.. code:: html

  <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.12.4/jquery.min.js"></script>


Configuration
-------------
The Camera Slider JS and CSS are by default loaded from the below CDN. If you wish to override this, this can be done in your settings.py file by adding the below with your updated URLs. This is optional. 

.. code:: python

    DJANGOCMS_CAMERASLIDER = {
        'JS_URL': 'https://cdnjs.cloudflare.com/ajax/libs/Camera/1.3.4/scripts/camera.min.js',
        'CSS_URL': 'https://cdnjs.cloudflare.com/ajax/libs/Camera/1.3.4/css/camera.min.css'
    }

Usage
------
The slider plugin is added to page, where the configuration for the slider is set. The settings allow you to add a carousel thumbnail slider if you wish, you are also provided the ability to pass the JSON config for both the carousel and the slider.

There are many `Camera Slider examples`_ on their site, or you can view the full `Camera Slider properties`_. The configuration JSON object is optional, so you have no obligation to provide this. A simple example of the config with a carousel is provided below.

Once the slider has been setup, slides are added by adding child slide plugins to the slider. Each slide has to have an image, (I've used `django-filer`_ for the images), and can optionally have an explicit height and/or width, a caption, url link or page link as well.


.. _django-cms: https://github.com/divio/django-cms
.. _Camera Slider: https://www.jqueryscript.net/slideshow/Camera-Slideshow-Plugin.html
.. _Camera Slider examples: https://www.jqueryscript.net/demo/Camera-Slideshow-Plugin/demo/
.. _Camera Slider properties: https://www.jqueryscript.net/slideshow/Camera-Slideshow-Plugin.html
.. _django-filer: https://github.com/divio/django-filer
.. _easy-thumbnails: https://github.com/SmileyChris/easy-thumbnails
.. _djangocms-text-ckeditor: https://github.com/divio/djangocms-text-ckeditor
