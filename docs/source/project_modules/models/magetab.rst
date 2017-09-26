.. magetab_models_ref:

MAGE-TAB Models
===============
MAGE-TAB consists of 3 files describing a microarray experiment - and recently sequencing experiments as well.
For each experiment there must be and **IDF (Investigation Description Format)** file and an **SDRF(Sample and Data Relationship Format)**.
For microarray experiment, an experiment must be connected to an **ADF (Array Design Format)** which contains
information about the microarray chip used in the study.

The fist 2 file formats has representing models in this package and their inline documentation are as follows:

:mod:`IDF Model`
-----------------

The main class is ``IDF`` which uses other 2 partial classes ``IDFElementSingle`` and ``IDFElementMultiple``

:class:`IDF`
+++++++++++++
.. autoclass:: models.magetab.idf.IDF
    :members:
    :undoc-members:
    :private-members:

:class:`IDFElementSingle`
++++++++++++++++++++++++++
.. autoclass:: models.magetab.idf.IDFElementSingle
    :members:
    :undoc-members:
    :private-members:

:class:`IDFElementMultiple`
++++++++++++++++++++++++++
.. autoclass:: models.magetab.idf.IDFElementMultiple
    :members:
    :undoc-members:
    :private-members:

