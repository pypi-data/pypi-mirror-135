=======================
Django Generic Search
=======================

Django Generic Search is a Django app to conduct generic search on your site's pages. Visitors on your site can search for any
available pages on your side given they new or can guess accurately keywords or search queries related to thos pages.

Detailed documentation is in the "docs" directory.

Quick start
-----------

Install the package using ``pip``.

.. code-block:: sh

	$ pip install django-generic-search

Add "django-generic-search" to your INSTALLED_APPS setting like this

.. code-block:: python

    INSTALLED_APPS = [
        ...
        'generic-search',
    ]

Include the django-generic-search URLconf in your project urls.py like this

.. code-block:: python

    path('search/', include('generic-search.urls')),

include settings below in project settings.py

.. code-block:: python

    ALLOWED_HOSTS = [
        'localhost',
    ]
    SPYDER_START_URLS = {
        'gammaspider': ['https://localhost:8000/']
    }

    When in production, update the settings above appropriately to reflect your production environment.

Run ``python manage.py crawlsite`` to create an index of the available pages on your site.

Start the development server and visit http://127.0.0.1:8000/

Visit http://127.0.0.1:8000/search/?q=<search-query> to retrieve search results.
