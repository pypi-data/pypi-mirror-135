.. easchersim documentation master file, created by
   sphinx-quickstart on Wed Jan 12 18:32:49 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.


Welcome to EASCherSim's documentation!
======================================

This is a simulation tool for the estimation of the optical Cherenkov signal produced in the atmosphere by an Extensive Air Shower.
The simulation includes atmospheric effect as well as the impact of the magnetic field. More details can be found in `[1] <https://arxiv.org/pdf/2011.09869>`_ for upawards 
going shower trajectories and in `[2] <https://arxiv.org/pdf/2105.03255>`_ for geometries above the limb.

The source code repository is available on `GitLab <https://gitlab.com/c4341/easchersim>`_.

Please provide feedback, bug reports, and feature requests through our public `Issue Tracker <https://gitlab.com/c4341/easchersim/-/issues>`_.

Paper to be cited if you use this program : `[PhysRevD.103.043017] <https://link.aps.org/doi/10.1103/PhysRevD.103.043017>`_, `[PhysRevD.104.063029] <https://journals.aps.org/prd/abstract/10.1103/PhysRevD.104.063029>`_

.. panels::
   :container: container-fluid pb-1
   :column: col-lg-6 col-md-6 col-sm-12 col-xs-12 p-2
   :card: text-center
   :img-top-cls: pl-5 pr-5

   ---
   :fa:`cogs` API reference
    ^^^^^^^^^^^^^
    The reference guide the methods work
    and which parameters can be used.
    +++

    .. link-button:: api/index
            :type: ref
            :text: To the API
            :classes: btn-block btn-secondary stretched-link

   ---
   :fa:`book` User guide
    ^^^^^^^^^^^^^
    The user guide provides information and 
    explanation of the use and background of 
    easchersim.
    +++

    .. link-button:: UserGuide/index
            :type: ref
            :text: To the user guide
            :classes: btn-block btn-secondary stretched-link



.. toctree::
   :hidden:

   API <api/index>
   User Guide <UserGuide/index>