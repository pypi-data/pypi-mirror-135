=============================
Django File Field Utils
=============================

.. image:: https://badge.fury.io/py/django-file-field-utils.svg/?style=flat-square
    :target: https://badge.fury.io/py/django-file-field-utils

.. image:: https://readthedocs.org/projects/pip/badge/?version=latest&style=flat-square
    :target: https://django-file-field-utils.readthedocs.io/en/latest/

.. image:: https://img.shields.io/coveralls/github/frankhood/django-file-field-utils/main?style=flat-square
    :target: https://coveralls.io/github/frankhood/django-file-field-utils?branch=main
    :alt: Coverage Status

This package is a set of field and widget that improves the images and files field behaviour

Documentation
-------------

The full documentation is at https://django-file-field-utils.readthedocs.io.

Quickstart
----------

Install Django File Field Utils::

    pip install django-file-field-utils

You need to add *easy_thumbnails* to `INSTALLED_APPS`:

.. code-block:: python

    INSTALLED_APPS = (
        ...
        'easy_thumbnails',
        ...
    )

Run

.. code-block:: python

    python manage.py migrate easy_thumbnails


Features
--------

* A image-field that support also svg files

**Example of usage**

.. code-block:: python

    image = SVGAndImageField(_("Image"), blank=True)

* An admin widget that get the preview of image-field


**Example of usage**

.. code-block:: python

    from file_field_utils.db.widgets import ConfigurableImageWidget

    class NewsAdminForm(forms.ModelForm):
        class Meta:
            model = News
            widgets = {
                'image': ConfigurableImageWidget()
            }

    @admin.register(News)
    class NewsAdmin(admin.ModelAdmin):
        form = NewsAdminForm

* Method for media file upload path support in file fields

**Example of usage**

.. code-block:: python

    image = ImageField(_("Image"), upload_to=UploadPath("example"), blank=True)

The image of model instance will be upload under directory:
    /media/uploads/<instance_model_app_label>/<instance_model_name>/example/


.. code-block:: python

    image = ImageField(_("Image"), upload_to=UploadPathWithID("example"), blank=True)

The image of model instance will be upload under directory:
    /media/uploads/<instance_model_app_label>/<instance_model_name>/example/<instance_id>/


Running Tests
-------------

Does the code actually work?

::

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

::

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

Tools used in rendering this package:

*  Cookiecutter_
*  `cookiecutter-djangopackage`_

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`cookiecutter-djangopackage`: https://github.com/pydanny/cookiecutter-djangopackage
