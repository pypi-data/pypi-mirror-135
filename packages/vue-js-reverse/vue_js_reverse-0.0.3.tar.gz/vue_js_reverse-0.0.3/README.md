=================
VUE JS Reverse
=================

**Vue url handling for Django that doesn’t hurt.**


Overview
--------

Django Vue Reverse (a fork of Django Js Reverse) is a small django app that makes url handling of
`named urls <https://docs.djangoproject.com/en/dev/topics/http/urls/#naming-url-patterns>`__ in javascript easy and non-annoying..

For example you can retrieve a named url:

urls.py:

::

    url(r'^/betterliving/(?P<category_slug>[-\w]+)/(?P<entry_pk>\d+)/$', 'get_house', name='betterliving_get_house'),

in javascript like:

::

    this.$urls.betterlivingGetHouse('house', 12)

Result:

::

    /betterliving/house/12/


Requirements
------------

python 3.6+


Installation
------------

Install using ``pip`` …

::

    pip install vue-js-reverse

… or clone the project from github.

::

    git clone https://github.com/miklagard/vue-js-reverse

Add ``'vue_js_reverse'`` to your ``INSTALLED_APPS`` setting.

::

    INSTALLED_APPS = (
        ...
        'vue_js_reverse',
    )

Add library variables to settings.py file.

::

    VUE_PLUGINS_DIR = os.path.join(settings.BASE_DIR, 'vue_frontend', 'src', 'plugins')
    VUE_REVERSE_URL_PLUGIN = 'Urls.js'

Vue main.js
------------------

::

     import Url from "@/plugins/Url"
     Vue.use(Url)


Usage as static file
--------------------

First generate static file by

::

    ./manage.py vue_js_reverse

If you change some urls or add an app and want to update the reverse.js file,
run the command again.

After this add the file to your template


License
-------

`MIT <https://raw.github.com/ierror/django-js-reverse/master/LICENSE>`__


Contact
-------

`@i_error <https://twitter.com/i_error>`__

--------------

Enjoy!
