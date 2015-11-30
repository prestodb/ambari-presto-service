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

import os.path as path

from resource_management import *

PRESTO_RPM_URL = 'http://sdvl3bdch001.td.teradata.com/RPMs/presto-server-rpm-0.114-1.x86_64.rpm'
PRESTO_RPM_NAME = PRESTO_RPM_URL.split('/')[-1]
PRESTO_CLI_URL = 'http://sdvl3bdch001.td.teradata.com/RPMs/presto-cli-0.114-executable.jar'
PRESTO_CLI_NAME = PRESTO_CLI_URL.split('/')[-1]

def create_tpch_connector(node_properties):
        Execute('mkdir -p {0}'.format(node_properties['plugin.config-dir']))
        Execute('echo "connector.name=tpch" > {0}'.format(path.join(node_properties['plugin.config-dir'], 'tpch.properties')))