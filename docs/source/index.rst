.. AE Auto documentation master file, created by
   sphinx-quickstart on Thu May 25 15:43:40 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

AE Automation
==============
AE Automation tool which is developed to automate some of the processes in ArrayExpress.
This project is developed to be used internally by AE team.
It is an n-tier python application that has different smaller packages that are being reused through the source code.
Most of the modules has command line interface and all the code parts can be reused in other external python apps.

In addition, there is also a |Django| application that exposes some functionality as `rest API` and as a web app.

In the next few sections, the overall design and implementation will be discussed
followed usage of the different modules and eventually the technical documentation and coding samples.

The source code can be found on |ae_github|.

.. |ae_github| raw:: html

   <a href="https://github.com/arrayexpress/ae-auto" target="_blank">ArrayExpress Github</a>

.. |Django| raw:: html

   <a href="https://www.djangoproject.com/" target="_blank"><i>Django<i></a>

Guide:
------

.. toctree::
    :name: mastertoc
    :glob:
    :maxdepth: 4

    structure




Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
