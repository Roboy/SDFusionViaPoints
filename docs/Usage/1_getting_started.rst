.. _getting_started:

Getting started
===============

Make sure that all links of the robot are defined as rigid groups and named correctly. For more information on how to correctly define the robot model see http://sdfusion.readthedocs.io/en/master/.

To run the script in Fusion, run the Script and Add-Ins command and select the SDFusionViaPoints addin. Click the "Run" button. A button with Roboy logo named Via-Points shows up in the left end of the 'MODEL'-taskbar in Fusion.

Please be aware, that the addin is currently being developed. Therefore full functionality is not given and the user is required to read :ref:`features` carefully.

.. _background_information_via_points:

Background information on Via-Points:
-------------------------------------

Via-Points are the points along which a tendon of the robot is routed. Correctly defined, they can be used **1)** as a documentation on where the tendons in the real robot are routed and **2)** as points in the simulation of the robot where forces are added.

For every Via-Point these parameters need to be known:
- MyoMuscle: To which myoMuscle this via-point belongs
- Link: On which link this via-point is fixed
- Number: the number of the via-point, so that the tendon runs from the muscle unit through the via-points with ascending numbers


.. _run_UI:

Running the User Interface:
---------------------------

To use the UI click on the Button with Roboy logo named Via-Points. This action needs to be performed for every myoMuscle to which  you want to  add via-points. A dialog window pops up. It is separated into three sections:

1. Select the number of the myoMucle for which you want to specify via-points.

2. Select the via-points you want to add. You can select thw number of the via-point and on which link it is fixed. The last input lets you select which of the **Selections** in the third part of the dialog window belong to the given via-point information. This is not the smoothest solution, but could not be solved better, because of restrictions in the Fusion API.

3. Select holes in the robot model in which the via-points are located. At the moment the selection is restricted to curved edges.

.. figure:: images/UI.png
  :alt: Screenshot of the Dialog Window

.. _clicking_OK:

Clicking OK:
------------

To create the new via-points for the robot model click **OK** in the dialog window. Fusion automatically creates arbitrarily named via-points (construction points) in the robot model, that can be exported by the SDFusion exporter.

.. _adapting_the_script:

Adapting the script
-------------------

The script should not be adapted by the user to its needs right now, as it is under heavy developement. In the future there will be the opportunity to hard-code the link names, so that no rigid groups need to be created for that.

.. _features:

Non-Features:
-------------

The via-points are only created, if all input fields in the dialog window are filled out. The link names are static and hard-coded at the moment.
