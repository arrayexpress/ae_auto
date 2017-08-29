Project Structure
=================

.. figure::  images/python_ae_package.png
   :align:   center

   AE Automation Packages


The diagram above shows the top level components of the project. It lists only the most important sub-components that are being discussed in detail in this documentation.



* Automation: This is the core package that has most used and important modules. This include:
    a. :ref:`ena`:  The module for ENA brokering pipeline.
        This module automates the process of submitting sequencing experiments to ENA.
    b. :ref:`ae_publication`: collecting, scoring and saving new publications appear on |europe_pmc|.
    c. :ref:`release_date`: Automate the processes related to the experiments’ release dates.
        The source of these requests might be one of the following:

            - ENA
            - GEO
            - Submitters
    d. :ref:`geo`: This module contains most of the processes related to GEO experiments. This includes:
            - Fixing SDRF after |GEO_NCBI| import. This process is used in the internal workflow engine Conan.
            - Importing Array Designs from |GEO_NCBI| and loading them into ArrayExpress in |adf|.


* :ref:`dal`: It is the only way to access different databases using both |gateway|, and |transaction_script| Transaction scripts. It has 2 main blocks according the the database type:

   a. MySQL: Contains all gateways and transaction scripts for each MySQL schema
   b. Oracle: Contains the gateways and transaction scripts for each Oracle Database.


* Resources: This package contains the scripts and tools required to access external services such as Europe PMC and ENA services.

* Settings: Contains the app settings like the database connection parameters, the physical paths for data on the shared storage ... etc.

* Utils: Contains shared utilities like email services, parsers, and wrappers to already existing tools like fastaq validators ...etc.

* Services: Exports different  functionality of the package as a REST web service to be used by other local tools.
 This can be added later after the core is developed by using Django REST Framework or any other alternative.


Modules
--------

.. toctree::
    :maxdepth: 2
    :glob:

    project_modules/automation/*
    project_modules/dal
    project_modules/geo




.. |europe_pmc| raw:: html

   <a href="https://europepmc.org/" target="_blank">Europe PMC</a>

.. |GEO_NCBI| raw:: html

   <a href="https://www.ncbi.nlm.nih.gov/geo/" target="_blank">GEO</a>

.. |adf| raw:: html

   <a href="https://www.ebi.ac.uk/arrayexpress/help/adf_submissions_overview.html" target="_blank">Table Data Gateways</a>

.. |gateway| raw:: html

   <a href="https://martinfowler.com/eaaCatalog/tableDataGateway.html" target="_blank">ADF format</a>
.. |transaction_script| raw:: html

   <a href="https://martinfowler.com/eaaCatalog/transactionScript.html" target="_blank">Transaction scripts</a>