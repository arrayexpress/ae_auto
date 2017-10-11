.. _ena_models_ref:

ENA Models
==========
These models encapsulate the ENA different data structure in a hierarchical model structure.
By creating an instance of ``ENAStudy`` with and existing ENA Accession number it will query the database
and retrieve all the related objects from ENA database an build the different structures. These models
are used by :ref:`add_ena_accessions_ref`.

:mod:`ENAStudy`
----------------

.. autoclass:: models.ena_models.ENAStudy
    :members:
    :undoc-members:
    :private-members:


:mod:`ENAExperiment`
---------------------

.. autoclass:: models.ena_models.ENAExperiment
    :members:
    :undoc-members:
    :private-members:
