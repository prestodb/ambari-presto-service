# ambari-presto-service

**Note: the integration code in this repo is still a work in progress. It may be lacking certain integration features and at times may break. Use at your own risk.**

This repo contains code and configuration needed to integrate [Presto](https://prestodb.io/) with [Ambari](https://ambari.apache.org/). Once you've deployed the integration code (for more details on this see [Integration instructions for users](#iifu)), you'll be able to do the following:

1. Install and deploy Presto to your cluster from the Ambari UI.
2. Configure all aspects of Presto via the Ambari UI.
3. Have dashboard access to some critical Presto and kernel level metrics.

## Requirements

1. Python 2.6/2.7.
2. Make.

## <a name="iifu"></a>Integration instructions for users

Unfortunately, at the moment Ambari does not support a more user friendly installation method. The installation has to be done by following the somewhat manual steps outlined below.

1. Create the distribution by executing `make clean dist`. This will create a `tar.gz` in the dist directory. This file is the distribution you'll need to upload to your cluster.
2. Upload the distribution archive to the node in your cluster that runs the Ambari master server.
3. Assuming that `ambari-server` is installed in `/var/lib/ambari-server`, you should execute the following:
```
mkdir /var/lib/ambari-server/resources/stacks/HDP/2.2/services/PRESTO
tar -xvf ambari-presto-0.1.0.linux-x86_64.tar.gz -C /var/lib/ambari-server/resources/stacks/HDP/2.2/services/PRESTO
chmod -R +x /var/lib/ambari-server/resources/stacks/HDP/2.2/services/PRESTO/*
ambari-server restart
```
4. Once the server has restarted, point your browser to it and on the main Ambari Web UI page click the `Add Service` button and follow the on screen wizard to add Presto.

## For developers

The following definitions, taken from the [Apache Ambari wiki](https://cwiki.apache.org/confluence/display/AMBARI/Stacks+and+Services), are useful when talking about integration:

1. Stack - Defines a set of Services and where to obtain the software packages for those Services. A Stack can have one or more version, and each version can be active/inactive. For example, Stack = HDP-2.3.
2. Service - Defines the Components (MASTER, SLAVE, CLIENT) that make up the Service. For example, Service = HDFS.
3. Component - The individual Components that adhere to a certain defined lifecycle (start, stop, install, etc). For example, Service = HDFS has Components = NameNode (MASTER), Secondary NameNode (MASTER), DataNode (SLAVE) and HDFS Client (CLIENT).

For more information on developing service integration code for Ambari, the following resources might be helpful:
1. [Webcast](http://hortonworks.com/partners/learn/#ambari) with Hortonworks engineers about integrating with Ambari. Includes slides and recorded video/audio of the talk.
2. Lots of [integration examples](https://github.com/abajwa-hw/ambari-workshops).

The build system for this project is very simple: we use Python's standard [distutils](https://docs.python.org/2/distutils/) module. We wrap calls to the `setup.py` script with a Makefile to make common actions even simpler. To build the distribution execute `make dist`, to run the unit tests execute `make test` and to get more information on the other availabel targets execute `make help`.

If you're having trouble with something feel free to file an issue. PRs are always welcome!