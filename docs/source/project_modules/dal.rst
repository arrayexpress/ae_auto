.. _dal_ref:

Data Access Layer (DAL)
======================
DAL is the only way of accessing databases in the whole application. There are 2 main packages namely ``mysql``
and ``oracle`` for the 2 db resources we have. Each of them contains list of packages for each db scheme we have.
These schema packages are simply direct implementation for |gateway| and |transaction_script| design pattern.



.. |gateway| raw:: html

   <a href="https://martinfowler.com/eaaCatalog/tableDataGateway.html" target="_blank"><i>Table Gate Way</i></a>

.. |transaction_script| raw:: html

   <a href="https://martinfowler.com/eaaCatalog/transactionScript.html" target="_blank"><i>Transaction Scripts</i></a>

.. _MySQL:

MySQL
------


:mod:`common`
+++++++++++++
This module contains basic DB connection and sql execution.

.. automodule:: dal.mysql.common
    :members:
    :undoc-members:
    :show-inheritance:


:mod:`ae_autosubs`
++++++++++++++++++

:mod:`experiments`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.mysql.ae_autosubs.experiments
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`annotare`
++++++++++++++++++


:mod:`data_files`
^^^^^^^^^^^^^^^^^^^^^^^^

.. automodule:: dal.mysql.annotare.data_files
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`submission`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.mysql.annotare.submission
    :members:
    :undoc-members:
    :show-inheritance:







.. _Oracle:

Oracle
----------------


:mod:`common`
+++++++++++++
This module contains basic DB connection and sql execution.

.. automodule:: dal.oracle.common
    :members:
    :undoc-members:
    :show-inheritance:
:mod:`ae2`
+++++++++++++


:mod:`ae2_transaction`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.ae2_transaction
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`contact`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.contact
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`plat_design`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.plat_design
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`publication`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.publication
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`study`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.study
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`study_publication`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.study_publication
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`view_publications`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.ae2.view_publications
    :members:
    :undoc-members:
    :show-inheritance:


:mod:`biostudies` 
+++++++++++++

:mod:`biostudies_transaction` 
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.biostudies.biostudies_transaction
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`conan` 
+++++++++++++


:mod:`conan_tasks` 
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.conan.conan_tasks
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`conan_transaction` 
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.conan.conan_transaction
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`conan_users` 
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.conan.conan_users
    :members:
    :undoc-members:
    :show-inheritance:


:mod:`era` 
+++++++++++++


:mod:`data_file_meta` 
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.data_file_meta
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`era_transaction`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.era_transaction
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`experiment`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.experiment
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`experiment_sample`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.experiment_sample
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`run`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.run
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`sample`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.sample
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`study`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.study
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`webin_file`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.webin_file
    :members:
    :undoc-members:
    :show-inheritance:

:mod:`wh_run`
^^^^^^^^^^^^^^^^^^

.. automodule:: dal.oracle.era.wh_run
    :members:
    :undoc-members:
    :show-inheritance:


