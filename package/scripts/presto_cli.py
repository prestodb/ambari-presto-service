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

from resource_management.libraries.script.script import Script
from resource_management.core.resources.system import Execute
from common import PRESTO_CLI_URL, PRESTO_CLI_NAME


class Cli(Script):
    def install(self, env):
        Execute('wget --no-check-certificate {0} -P /usr/lib/presto/bin'.format(PRESTO_CLI_URL))
        Execute('chmod +x /usr/lib/presto/bin/{0}'.format(PRESTO_CLI_NAME))
        Execute('mv /usr/lib/presto/bin/{0} /usr/lib/presto/bin/presto-cli'.format(PRESTO_CLI_NAME))

    def status(self, env):
        pass

    def configure(self, env):
        # Actual configuration is done in the master and worker configure() methods
        pass

if __name__ == '__main__':
    Cli().execute()