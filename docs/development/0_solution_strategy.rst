.. _solution_strategy:

Solution Strategy
=================

General Strategy
----------------

Using the Autodesk Fusion API you have access to nearly all information stored for a robot model and you can modify the model like you can in direct interaction with Autodesk Fusion.

The addin uses events and event handlers to manage user input. As soon as the user clicks the via-point button, the dialog window pops up and collects all information needed to add the via-points to the robot model. As soon as the user dialog is closed the via-points are created and added to the model.