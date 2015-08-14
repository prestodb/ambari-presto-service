import socket
import os.path as path

from resource_management import *

class Master(Script):
    def install(self, env):
        Execute('wget sdvl3bdch001.td.teradata.com/RPMs/presto-server-rpm-0.114-1.x86_64.rpm -P /tmp')
        Execute('rpm -i /tmp/presto-server-rpm-0.114-1.x86_64.rpm')
        self.configure(env)

    def stop(self, env):
        from params import daemon_control_script
        Execute('{0} stop'.format(daemon_control_script))

    def start(self, env):
        from params import daemon_control_script
        Execute('{0} start'.format(daemon_control_script))

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
                f.write(key_val_template.format(key, value))
            f.write(key_val_template.format('coordinator', 'true'))
            f.write(key_val_template.format('discovery-server.enabled', 'true'))

if __name__ == '__main__':
    Master().execute()
