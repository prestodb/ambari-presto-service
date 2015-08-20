import os.path as path

from resource_management import *

def create_tpch_connector(node_properties):
        Execute('mkdir -p {0}'.format(node_properties['plugin.config-dir']))
        Execute('echo "connector.name=tpch" > {0}'.format(path.join(node_properties['plugin.config-dir'], 'tpch.properties')))