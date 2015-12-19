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

from unittest import TestCase
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from package.scripts.presto_cli import Cli

class TestCli(TestCase):

    def setUp(self):
        self.presto_cli = Cli()
        self.mock_env = MagicMock()

    @patch('package.scripts.presto_cli.Execute')
    def test_install_shells_out_to_execute(self, execute_mock):
        self.presto_cli.install(MagicMock)

        assert execute_mock.called

    # Raising ClientComponentHasNoStatus is needed so that restart
    # functionality works.
    def test_status_raises_exception(self):
        try:
            self.presto_cli.status(self.mock_env)
        except Exception as e:
            self.assertEqual(repr(e), 'ClientComponentHasNoStatus()')
            return
        TestCase.fail(self)

    # Client must implement status, configure, start and stop even
    # if those methods don't make sense for the component. They must
    # be implement for restart functionality to work correctly.
    def test_methods_overriden(self):
        assert 'configure' in dir(self.presto_cli)
        assert 'start' in dir(self.presto_cli)
        assert 'stop' in dir(self.presto_cli)
        assert 'status' in dir(self.presto_cli)