.. contents::

Introduction
============

Locales package for cpskin


Translations
------------

The cpskin product has been translated into

- Deutsch.

- Spanish.

- French.

- Nederlands.


Usage
=====

To find untranslated strings, run ::

    bin/i18ncheck

To generate and merge translations (there are 3 domains), run ::

    bin/i18n plone
    bin/i18n plone.app.event
    bin/i18n cpskin

Be aware that all .py files are excluded of plone and plone.app.event domains
and that cpskin.agenda is the only package included when generating
plone.app.event domain files.


Transifex.net
-------------

You can help for contributing translations for unsupported messages.

The cpskin project welcomes the speakers from the world to translate
any messages, which is not supported yet.

Alternative, the cpskin product has *Transifex.net* integration to 
help you perform all translations faster and easier collaboratively 
with multiple translators from the `Plone community <https://plone.org/>`_.

You can contribute to translate messages into avaliable languages at
`Transifex.net <https://www.transifex.com/plone/plonegov-imio/>`_.

When you done your translation resource at Transifex.net, you need to add 
the locales files into cpskin project, for that you need use 
`transifex-client <https://docs.transifex.com/client/introduction>`_ tool 
and `install it <https://docs.transifex.com/client/installing-the-client>`_.


Tests
=====

This package is tested using Travis CI. The current status is :

.. image:: https://travis-ci.org/IMIO/cpskin.locales.png
    :target: http://travis-ci.org/IMIO/cpskin.locales
