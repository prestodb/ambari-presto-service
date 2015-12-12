# ambari-presto-service

This repository contains the code and configuration needed to integrate [Presto](https://prestodb.io/) with [Ambari](https://ambari.apache.org/). Adding the Presto service to Ambari allows:

1. Installing and deploying Presto on a cluster from the Ambari UI.
2. Changing Presto configuration options via the Ambari UI.

# Table of contents

* [Getting Started](#getting-started)
  * [Requirements for integration](#requirements-for-integration)
  * [Adding the Presto service](#adding-the-presto-service)
  * [Supported topologies](#supported-topologies)
    * [Pseudo-distributed](#pseudo-distributed)
    * [Distributed](#distributed)
  * [Configuring Presto](#configuring-presto)
    * [Adding and removing connectors](#adding-and-removing-connectors)
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

This section and all others that follow within [Getting Started](#getting-started) walk you through the integration steps needed to get Presto working with Ambari. By default, this integration code installs Presto version `0.127t`. To change the distribution to install another version, see [Build and custom distributions](#build-and-custome-distributions).

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

The following two screens will allow you to assign the Presto processes among the nodes in your cluster.

Presto is composed of a coordinator and worker processes. The same code runs all nodes because the same Presto server RPM is installed for both workers and coordinator. It is the configuration on each node that determines how a particular node will behave. Presto can run in pseudo-distributed mode, where a single Presto process on one node acts as both coordinator and worker, or in distributed mode, where the Presto coordinator runs on one node and the Presto workers run on other nodes.

The client component of Presto is the `presto-cli` executable JAR. You should place it on all nodes where you expect to access the Presto server via this command line utility. The `presto-cli` executable JAR does not need to be co-located with either a worker or a coordinator, it can be installed on its own. Once installed, the CLI can be found at `/usr/lib/presto/bin/presto-cli`.

*Do not place a worker on the same node as a coordinator.* Such an attempt will fail the installation because the integration software will attempt to install the RPM twice. In order to schedule work on the Presto coordinator, effectively turning the process into a dual worker/coordinator, please enable the `node-scheduler.include-coordinator` toggle available in the configuration screen.

### Pseudo-distributed

Pick a node for the Presto coordinator and *do not assign any Presto workers*. On the configuration screen that follows, you must also enable pseudo-distributed mode by clicking the toggle. If you assign Presto workers to nodes and enable the pseudo-distributed toggle, the installation will fail.

### Distributed

Pick a node for the Presto coordinator and assign as many Presto workers to nodes as you'd like. Feel free to also place the client component on any node. Remember to not place a worker on the same node as a coordinator.

## Configuring Presto

The one configuration property that does not have a default and requires input is `discovery.uri`. The expected value is `http://<FQDN-of-node-hosting-coordinator>:8081`. Note that it is http and not https and that the port is 8081. If you change the value of `http-server.http.port`, make sure to also change it in `disovery.uri`.

Some of the most popular properties are displayed in the Settings tab (open by default). In the Advanced tab, set custom properties by opening up the correct drop down and specifying a key and a value. Note that specifying a property that Presto does not recognize will cause the installation to finish with errors as some or all servers fail to start.

Change the Presto configuration after installation by selecting the Presto service followed by the Configs tab. After changing a configuration option, restart Presto for the changes to take effect. *Unfortunately, the orange/yellow Restart button that appears after the new configuration is saved, does not work. To restart Presto, navigate to each host and restart the component from there. We have contacted Hortonworks about this and are awaiting a fix/workaround.*

### Adding and removing connectors

To add a connector modify the `connectors.to.add` property, whose format is the following: `'{'connector1': ['key1=value1', 'key2=value2', etc.], 'connector2': ['key3=value3', 'key4=value4'], etc.}'`. Note the single quotes around the whole property and around each individual element. This property only adds connectors and will not delete connectors. Thus, if you add connector1, save the configuration, restart Presto, then specify {} for this property, connector1 will not be deleted.

To delete a connector modify the `connectors.to.delete` property, whose format is the following: `'['connector1', 'connector2', etc.]'`. Again, note the single quotes around the whole property and around each element. The above value will delete connectors `connector1` and `connector2`.

# Getting help

If you're having trouble with anything, please file an issue and we'll try our best to help you out.

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

The build system for this project is very simple; it uses Python's standard [distutils](https://docs.python.org/2/distutils/) module. Calls to the `setup.py` script are wrapped with a Makefile to make common operations simple. Execute `make dist` to build the distribution, `make test` to run the unit tests and `make help` to get more info on all the available targets.

By default, the integration code installs Teradata's `0.127t` version of Presto. Change the version displayed by Ambari when adding the Presto service by specifying a value for the `VERSION` variable when building the distribution. For example, to display Presto version `0.130`, run `make dist VERSION=0.130`. To download a different RPM and CLI to match version `0.130`, edit the `package/sctips/download.ini` file with URLs for both.
