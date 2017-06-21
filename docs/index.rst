.. Software Documentation template master file, created by
   sphinx-quickstart on Fri Jul 29 19:44:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

.. _welcome:

Welcome to SDFusionViaPoints!
===========================================================

This project provides an user interface for Autodesk Fusion 360, that ĺets users easily add and modify muscle via-points. The SDFusion exporter (links see below) is able to parse these via-points into SDFormat. This is used to simulate our tendon-driven robots.

The user interface itself is a python addin, which needs to be loaded into Autdesk Fusion 360 and executed.

SDFusion exporter:
- Repository https://github.com/Roboy/SDFusion
- Documentation http://sdfusion.readthedocs.io/en/master/

.. _background_prerequisits:

Relevant Background Information and Pre-Requisits
--------------------------------------------------

**Use:**

To use this addon you need a machine running Windows with Autodesk Fusion 360 installed. Furthermore your robot model needs to be in Fusion.

**Develop:**

To develop this addon further you need to be familiar with python, the SDFormat and our custon definition of via-points in it and the Autodesk Fusion API. You can find the Fusion API User's and Reference Manual here: http://help.autodesk.com/view/fusion360/ENU/?guid=GUID-A92A4B10-3781-4925-94C6-47DA85A4F65A .

Helpful Links:

- Autodesk Fusion 360		http://www.autodesk.de/products/fusion-360/overview
- SDFormat 					http://sdformat.org/
- Gazebo 					http://gazebosim.org/

.. _requirements_overview:

Requirements Overview
---------------------

The **software requirements** define the system from a blackbox/interfaces perspective. They are split into the following sections:

- **User Interfaces** - :ref:`user_interfaces`
- **Technical Interfaces** - :ref:`technical_interfaces`
- **Runtime Interfaces and Constraints** - :ref:`runtime_interfaces`

Contents:

.. _usage:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Usage and Installation

  Usage/*

.. _ScopeContext:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Interfaces and Scope

  ScopeContext/*

.. _development:
.. toctree::
  :maxdepth: 1
  :glob:
  :caption: Development

  development/*

.. toctree::
   :maxdepth: 1

   about-arc42
