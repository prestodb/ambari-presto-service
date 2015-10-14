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

from mock import Mock, patch

import unittest
import sys
sys.modules['resource_management'] = Mock()
sys.modules['resource_management.core'] = Mock()
sys.modules['resource_management.core.resources'] = Mock()
sys.modules['resource_management.core.resources.system'] = Mock()

sys.modules['resource_management.libraries'] = Mock()
sys.modules['resource_management.libraries.script'] = Mock()
sys.modules['resource_management.libraries.script.script'] = Mock()

from package.scripts.presto_worker import Worker


class TestWorker(unittest.TestCase):

    def setUp(self):
        self.mock_env = Mock()

    def test_start(self):
        presto_worker = Worker()
        presto_worker.install(self.mock_env)
