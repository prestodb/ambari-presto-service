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

from mock import MagicMock, patch

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from package.scripts.presto_cli import Cli

class TestCli(unittest.TestCase):

    @patch('package.scripts.presto_cli.Execute')
    def test_install_shells_out_to_execute(self, execute_mock):
        presto_cli = Cli()

        presto_cli.install(MagicMock)

        assert execute_mock.called
