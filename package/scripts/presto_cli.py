from resource_management import *

class Cli(Script):
    def install(self, env):
        Execute('wget sdvl3bdch001.td.teradata.com/RPMs/presto-cli-0.114-executable.jar -P /usr/lib/presto/bin')
        Execute('chmod +x /usr/lib/presto/bin/presto-cli-0.114-executable.jar')
        Execute('mv /usr/lib/presto/bin/presto-cli-0.114-executable.jar /usr/lib/presto/bin/presto-cli')

    def status(self, env):
        pass

    def configure(self, env):
        # Actual configuration is done in the master and worker configure() methods
        pass

if __name__ == '__main__':
    Cli().execute()
