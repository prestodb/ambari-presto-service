class Script(object):

    def execute(self):
        pass

    @staticmethod
    def get_config():
        return {'configurations':
                {'node.properties': {},
                 'jvm.config': {'jvm.config': ''},
                 'config.properties': {}}}
