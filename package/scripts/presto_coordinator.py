# -*- coding: utf-8 -*-
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import socket
import os.path as path

from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from common import create_tpch_connector, PRESTO_RPM_URL, PRESTO_RPM_NAME
from presto_client import smoketest_presto, PrestoClient

class Coordinator(Script):
    def install(self, env):
        Execute('wget {0}  -O /tmp/{1}'.format(PRESTO_RPM_URL, PRESTO_RPM_NAME))
        Execute('rpm -i /tmp/{0}'.format(PRESTO_RPM_NAME))
        self.configure(env)

    def stop(self, env):
        from params import daemon_control_script
        Execute('{0} stop'.format(daemon_control_script))

    def start(self, env):
        from params import daemon_control_script, config_properties
        self.configure(env)
        Execute('{0} start'.format(daemon_control_script))
        smoketest_presto(PrestoClient('localhost', 'root',
                                      config_properties['http-server.http.port']))

    def status(self, env):
        from params import daemon_control_script
        Execute('{0} status'.format(daemon_control_script))

    def configure(self, env):
        from params import node_properties, jvm_config, config_properties, \
            config_directory
        key_val_template = '{0}={1}\n'

        with open(path.join(config_directory, 'node.properties'), 'w') as f:
            for key, value in node_properties.iteritems():
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('node.id', socket.gethostname()))

        with open(path.join(config_directory, 'jvm.config'), 'w') as f:
            f.write(jvm_config['jvm.config'])

        with open(path.join(config_directory, 'config.properties'), 'w') as f:
            for key, value in config_properties.iteritems():
                if key == 'query.queue-config-file' and value.strip() == '':
                    continue
                # ignore as it's not an actual config property, just
                # the user visible equivalent to node-scheduler.include-coordinator
                if key == 'pseudo.distributed.enabled':
                    continue
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('coordinator', 'true'))
            f.write(key_val_template.format('discovery-server.enabled', 'true'))
            if config_properties['pseudo.distributed.enabled']:
                f.write(key_val_template.format(
                    'node-scheduler.include-coordinator', 'true'))

        create_tpch_connector(node_properties)

if __name__ == '__main__':
    Coordinator().execute()
