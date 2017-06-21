.. _design_decisions:

Design Decisions
================

The script adds construction points to the robot model. These are used to represent the tendon via-points.

Adding all via-points per muscle:
---------------------------------

The dialog window was designed with the lazy user in mind. Therefore it was tried to reduce the number of clicks the user needs to perform. This led to the decision to make it possible to export all via-points of one myoMuscle in on dialog window and to **NOT** use one dialog window per via-point to add.

Selecting the via-point position
--------------------------------

The dialog window is internally handled as a table with different input methods, e.g. a integer value spinner for the via-point number or a dropdown menu to select the link to which the via-point is fixed. Unfortuately this table can not hold selection inputs. Therefore the user can only specify which of the selection inputs belongs to the rest of the data in one of the table's rows. The selection of the via-points position then needs to be done in a separate part of the dialog window.