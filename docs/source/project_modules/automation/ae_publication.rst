.. _ae_publication:

AE Publication
===============
This module is responsible for importing publications form |europe_pmc| associated with ArrayExpress experiments.
It uses the Europe PMC |pmc_rest| - client implementation is :doc:`here <../resources/europe_pmc>`- to collect all
articles mentioning `ArrayExpress`.

After that, articles are filtered based by calling |tmt| endpoint of the rest API and execluding those articles
having no AE accessions in their text-mined terms.

Then, the filtered list is then compared with what is existed in the database, and hence create the proper
type of association between an article and an experiment which is then reviewed - approved or rejected- by
curators using the :doc:`web app <../ae_web/ae_web>` of this project.

Code and Inline Documentation
------------------------------


:mod:`publications_experiments`
++++++++++++++++++++++++++++++

.. automodule:: automation.ae_publications.publications_experiments
    :members:
    :undoc-members:
    :show-inheritance:

.. |europe_pmc| raw:: html

   <a href="https://europepmc.org/" target="_blank">Europe PMC</a>

.. |pmc_rest| raw:: html

   <a href="https://europepmc.org/RestfulWebService" target="_blank">rest API</a>

.. |tmt| raw:: html

   <a href="https://europepmc.org/RestfulWebService#tmTerms" target="_blank">text-mined terms</a>