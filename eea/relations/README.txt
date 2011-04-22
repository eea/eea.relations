EEA Relations
=============
EEA Relations package redefines relations in Plone. Right now in Plone any
object can be in relation with any other object. EEA Relations lets you to
define possible relations between objects. EEA Relations also comes with a nice,
customizable faceted navigable popup for relations widget.

.. contents::

Installation
------------

The easiest way to get eea.relations support in Plone 4 using this package is to
work with installations based on `zc.buildout`_.  Other types of installations
should also be possible, but might turn out to be somewhat tricky.

To get started you will simply need to add the package to your "eggs" and
"zcml" sections, run buildout, restart your Plone instance and install the
"eea.relations" package using the quick-installer or via the "Add-on
Products" section in "Site Setup".

  .. _`zc.buildout`: http://pypi.python.org/pypi/zc.buildout/

You can download a sample buildout at:

  http://svn.eionet.europa.eu/repositories/Zope/trunk/eea.relations/buildouts/plone4/

Dependencies
------------

  * graphviz

      yum install graphviz

      apt-get install graphviz

Documentation
-------------

  See the **doc** directory in this package.


API Doc
-------

  http://apidoc.eea.europa.eu/eea.relations-module.html


Authors
-------

  - "European Environment Agency", webadmin at eea europa eu
