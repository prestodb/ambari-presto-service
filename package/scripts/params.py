#!/usr/bin/env python

from resource_management import *

# config object that holds the configurations declared in the config xml file
config = Script.get_config()

node_properties = config['configurations']['node.properties']
jvm_config = config['configurations']['jvm.config']
config_properties = config['configurations']['config.properties']

daemon_control_script = '/etc/init.d/presto'
config_directory = '/etc/presto'
