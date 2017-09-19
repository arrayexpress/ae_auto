.. _resources

Resources
=========
This module is where are the used resources and API's clients are. The following resources are included:
    1. :ref:`conan_serv`
    2. :ref:`pmc_serv`
    3. :ref:`eutils_serv`


.. _conan_serv:

Conan
-----
This module calls the internal Conan2 rest API.

.. automodule:: resources.conan
    :members:
    :undoc-members:
    :show-inheritance:

.. _pmc_serv:

Europe PMC
----------
This modules is a client for |europe_pmc| |pmc_rest|

.. automodule:: resources.europe_pmc
    :members:
    :undoc-members:
    :show-inheritance:


.. _eutils_serv:

EUtils
-------
This module is a client for |ncbi| |eutils|

.. automodule:: resources.eutils
    :members:
    :undoc-members:
    :show-inheritance:


.. |europe_pmc| raw:: html

   <a href="https://europepmc.org/" target="_blank">Europe PMC</a>

.. |pmc_rest| raw:: html

   <a href="https://europepmc.org/RestfulWebService" target="_blank">rest API</a>

.. |ncbi| raw:: html

   <a href="https://www.ncbi.nlm.nih.gov/" target="_blank">NCBI</a>

.. |eutils| raw:: html

   <a href="https://www.ncbi.nlm.nih.gov/books/NBK25501/" target="_blank">Entrez Programming Utilities (E-Utilities)</a>
