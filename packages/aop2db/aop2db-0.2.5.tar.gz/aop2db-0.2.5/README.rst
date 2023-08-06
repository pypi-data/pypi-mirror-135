====================================================
AOP2DB |docs| |python_versions| |travis| |coverage|
====================================================

Package for compiling the adverse outcome pathway (AOP) data into a relational database. The data is publicly available at the `AOP website <https://aopwiki.org/>`_.

Installation |pypi_version| |pypi_license|
==========================================

``aop2db`` can be directly installed from PyPi with pip::

    $ pip install aop2db

Usage
=====

To load the data into a relational database::

    $ aop2db load

To set the driver of your database::

    $ aop2db conn mysql+pymysql://<user>:<password>@<server>/<database>

Disclaimer
==========
AOP2DB is a scientific software that has been developed in an academic capacity, and thus comes with no warranty or
guarantee of maintenance, support, or back-up of data.


.. |pypi_version| image:: https://img.shields.io/pypi/v/aop2db.svg
    :target: https://pypi.python.org/pypi/aop2db
    :alt: Current version on PyPI

.. |python_versions| image:: https://img.shields.io/pypi/pyversions/aop2db.svg
    :alt: Stable Supported Python Versions

.. |travis| image:: https://app.travis-ci.com/brucetony/aop2db.svg?branch=master
    :alt: Current build status

.. |docs| image:: https://readthedocs.org/projects/aop2db/badge/?version=latest
        :target: https://readthedocs.org/projects/aop2db/badge/?version=latest
        :alt: Documentation Status

.. |pypi_license| image:: https://img.shields.io/pypi/l/aop2db.svg
    :alt: MIT

.. |coverage| image:: https://codecov.io/gh/brucetony/aop2db/branch/master/graphs/badge.svg?
    :alt: Coverage Status