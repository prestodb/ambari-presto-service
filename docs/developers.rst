Developers
==========

Requirements for development
----------------------------

1. Python 2.6/2.7.
2. `pip <https://pip.pypa.io/en/stable/installing/>`_.
3. `make <https://www.gnu.org/software/make/>`_.
4. ``pip install -r $(REPO_ROOT_DIR)/requirements.txt``.

Definitions
-----------

The following definitions, taken from the `Apache Ambari wiki <https://cwiki.apache.org/confluence/display/AMBARI/Stacks+and+Services>`_,
are useful when talking about integration:

1. Stack - Defines a set of Services and the location where to obtain the
   software packages for those Services. A Stack can have one or more version,
   and each version can be active/inactive. For example, Stack = HDP-2.3.
2. Service - Defines the Components (MASTER, SLAVE, CLIENT) that make up the
   Service. For example, Service = HDFS.
3. Component - The individual Components that adhere to a certain defined
   lifecycle (start, stop, install, etc). For example, Service = HDFS has
   Components = NameNode (MASTER), Secondary NameNode (MASTER), DataNode
   (SLAVE) and HDFS Client (CLIENT).

Information on integrating services with Ambari
-----------------------------------------------

For more information on developing service integration code for Ambari, the
following resources might be helpful:

1. `Webcast <http://hortonworks.com/partners/learn/#ambari>`_ with Hortonworks
   engineers about integrating with Ambari. Includes slides and recorded
   video/audio of the talk.
2. Lots of `integration examples <https://github.com/abajwa-hw/ambari-workshops>`_.

.. _build_and_custom_distributions:

Build and custom distributions
------------------------------

The build system for this project is very simple; it uses Python's standard
`distutils <https://docs.python.org/2/distutils/>`_ module. Calls to the
``setup.py`` script are wrapped with a Makefile to make common operations
simple. Execute ``make dist`` to build the distribution, ``make test`` to run
the unit tests and ``make help`` to get more info on all the available
targets.

By default, the integration code installs Presto version ``0.196``. Change the
version displayed by Ambari when adding the Presto service by specifying a
value for the ``VERSION`` variable when building the distribution. For
example, to display Presto version ``0.134``, run ``make dist VERSION=0.134``.
To download a different RPM and CLI to match version ``0.134``, edit the
``package/scripts/download.ini`` file with URLs for both.
