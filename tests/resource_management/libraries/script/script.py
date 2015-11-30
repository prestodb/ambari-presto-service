class Script(object):

    def execute(self):
        pass

    @staticmethod
    def get_config():
        return {'configurations':
                {'node.properties': {},
                 'jvm.config': {'jvm.config': ''},
                 'config.properties': {},
                 'connectors.properties': {'connectors.to.add': '{}'}},
                 'clusterHostInfo': {'presto_worker_hosts': [], 'presto_coordinator_hosts': []}}