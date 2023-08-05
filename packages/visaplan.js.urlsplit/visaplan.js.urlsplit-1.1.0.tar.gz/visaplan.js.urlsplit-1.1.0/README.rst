.. This README is meant for consumption by humans and pypi. Pypi can render rst files so please do not use Sphinx features.
   If you want to learn more about writing documentation, please check out: http://docs.plone.org/about/documentation_styleguide.html
   This text does not appear on pypi or github. It is a comment.

====================
visaplan.js.urlsplit
====================

This is a simple Zope_ / Plone_ integration of the `urlSplit.js`_ Javascript tool
which provides a ``urlSplit(url_string)`` function.

Features
--------

- Makes available both the compressed and uncompressed versions of ``urlSplit.js``
- Adds the compressed version to the Javascript registry


Documentation
-------------

For the Javascript functionality, please see urlSplit.js_.


Installation
------------

Install visaplan.js.urlsplit by adding it to your buildout::

    [buildout]

    ...

    eggs =
        visaplan.js.urlsplit


and then running ``bin/buildout``.

After restarting your Zope instance, install the extension using the ``/prefs_install_products_form``.


As a dependency
~~~~~~~~~~~~~~~

- Add the package to your package dependencies, e.g. in your ``setup.py``::

    ...
    install_requires=[
        'setuptools',
        'visaplan.js.urlsplit',
        ],
    ...

- Add the package to your profile dependencies, e.g. in your ``…/profiles/default/metadata.xml``::

    <version>1000</version>
    <dependencies>
      <dependency>profile-visaplan.js.urlsplit:default</dependency>
    </dependencies>

- Restart your Zope instance and re-install your package.


Contribute
----------

For the Javascript functionality, please contribute to `urlSplit.js`_.

For the Zope / Plone integration:

- Issue Tracker: https://github.com/visaplan/js.urlsplit/issues
- Source Code: https://github.com/visaplan/js.urlsplit


License
-------

The project is licensed under the MIT License.

.. _Zope: https://www.zope.org
.. _Plone: https://plone.org
.. _`urlSplit.js`: https://github.com/hans-sperling/urlSplit.js
