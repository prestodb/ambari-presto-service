# ambari-presto-service

This repository contains code and configuration needed to integrate [Presto](https://prestodb.io/) with [Ambari](https://ambari.apache.org/). The integration packages allows you to:

1. Install and deploy Presto on your cluster from the Ambari UI.
2. Change Presto configuration options via the Ambari UI.

# Table of contents

* [Getting Started](#getting-started)
  * [Requirements for integration](#requirements-for-integration)
  * [Adding the Presto service](#adding-the-presto-service)
  * [Supported topologies](#supported-topologies)
    * [Pseudo-distributed](#pseudo-distributed)
    * [Distributed](#distributed)
  * [Configuring Presto](#configuring-presto)
    * [Adding and removing connectors](#adding-and-removing-connectors)
    * [Adding and removing unlisted properties](#adding-and-removing-unlisted-properties)
* [Getting help](#getting-help)
* [Developers](#developers)
  * [Requirements for development](#requirements-for-development)
  * [Definitions](#definitions)
  * [Information on integrating services with Ambari](#information-on-integrating-services-with-ambari)
  * [Build and custom distributions](#build-and-custome-distributions)

# Getting Started

## Requirements for integration

1. You must have Ambari installed and thus transitively fulfill [Ambari's requirements](http://docs.hortonworks.com/HDPDocuments/Ambari-2.1.2.1/bk_Installing_HDP_AMB/content/_meet_minimum_system_requirements.html).
2. Oracle Java JDK 1.8 (64-bit). Note that when installing Ambari you will be prompted to pick a JDK. You can tell Ambari to download Oracle JDK 1.8 or point it to an existing installation. Presto picks up whatever JDK Ambari was installed with so it is imperative that Ambari is running on Oracle JDK 1.8.

## Adding the Presto service

This section and all others that follow within [Getting Started](#getting-started) walk you through the integration steps needed to get Presto working with Ambari.

Unfortunately, at the moment Ambari does not support a more user friendly installation method and the installation has to be done by following the somewhat manual steps outlined below.

1. Assuming HDP 2.3 was installed with Ambari, create the following directory on the node where the `ambari-server` is running:
```bash
$ mkdir /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO
$ cd /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO
```
2. Place the integration files within the newly created PRESTO directory. Download the integration package from [here](https://s3-us-west-2.amazonaws.com/ambari-installation/ambari-presto-0.1.0.tar.gz) (TODO: swap in Teradata link), upload it to your cluster and extract it like so:
```bash
$ tar -xvf /path/to/integration/package/ambari-presto-0.1.0.tar.gz -C /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO
$ mv /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO/ambari-presto-0.1.0/* /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO
$ rm -f /var/lib/ambari-server/resources/stacks/HDP/2.3/services/PRESTO/ambari-presto-0.1.0
```
3. Finally, make all integration files executable and restart the Ambari server:
```bash
$ chmod -R +x /var/lib/ambari-server/resources/stacks/HDP/2.2/services/PRESTO/*
$ ambari-server restart
```
4. Once the server has restarted, point your browser to it and on the main Ambari Web UI page click the `Add Service` button and follow the on screen wizard to add Presto. The following sections provide more details on the options and choices you will make when adding Presto.

## Supported topologies

### Pseudo-distributed

### Distributed

## Configuring Presto

### Adding and removing connectors

### Adding and removing unlisted properties

# Getting help

# Developers

## Requirements for development

1. Python 2.6/2.7.
2. [pip](https://pip.pypa.io/en/stable/installing/).
3. [make](https://www.gnu.org/software/make/).
4. `pip install -r $(REPO_ROOT_DIR)/requirements.txt`.

## Definitions

The following definitions, taken from the [Apache Ambari wiki](https://cwiki.apache.org/confluence/display/AMBARI/Stacks+and+Services), are useful when talking about integration:

1. Stack - Defines a set of Services and where to obtain the software packages for those Services. A Stack can have one or more version, and each version can be active/inactive. For example, Stack = HDP-2.3.
2. Service - Defines the Components (MASTER, SLAVE, CLIENT) that make up the Service. For example, Service = HDFS.
3. Component - The individual Components that adhere to a certain defined lifecycle (start, stop, install, etc). For example, Service = HDFS has Components = NameNode (MASTER), Secondary NameNode (MASTER), DataNode (SLAVE) and HDFS Client (CLIENT).

## Information on integrating services with Ambari

For more information on developing service integration code for Ambari, the following resources might be helpful:
1. [Webcast](http://hortonworks.com/partners/learn/#ambari) with Hortonworks engineers about integrating with Ambari. Includes slides and recorded video/audio of the talk.
2. Lots of [integration examples](https://github.com/abajwa-hw/ambari-workshops).

## Build and custom distributions

The build system for this project is very simple: we use Python's standard [distutils](https://docs.python.org/2/distutils/) module. We wrap calls to the `setup.py` script with a Makefile to make common actions even simpler. To build the distribution execute `make dist`, to run the unit tests execute `make test` and to get more information on the other availabel targets execute `make help`.

If you're having trouble with something feel free to file an issue. PRs are always welcome!
