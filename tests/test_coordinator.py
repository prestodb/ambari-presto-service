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

from mock import MagicMock, patch, mock_open

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from package.scripts.presto_coordinator import Coordinator
from test_worker import mock_file_descriptor_write_method

class TestCoordinator(unittest.TestCase):

    dummy_config_properties = {'pseudo.distributed.enabled': 'true',
                               'query.queue-config-file': '',
                               'http-server.http.port': '8081',
                               'task.max-memory': '1GB'}

    def setUp(self):
        self.mock_env = MagicMock()

    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    @patch('package.scripts.presto_coordinator.smoketest_presto')
    @patch('package.scripts.presto_coordinator.Coordinator.configure')
    @patch('package.scripts.presto_coordinator.Execute')
    def test_lifecycle_methods_shell_out_to_execute(
            self, execute_mock, unused_configure_mock, unused_smoketest_presto):
        presto_coordinator = Coordinator()

        presto_coordinator.install(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_coordinator.stop(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_coordinator.start(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_coordinator.status(self.mock_env)
        assert execute_mock.called

    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    @patch('package.scripts.presto_coordinator.smoketest_presto')
    @patch('package.scripts.presto_coordinator.Coordinator.configure')
    @patch('package.scripts.presto_coordinator.Execute')
    def test_install_start_configure_presto(
            self, unused_execute_mock, configure_mock, unused_smoketest_presto):
        presto_coordinator = Coordinator()

        presto_coordinator.install(self.mock_env)
        assert configure_mock.called
        configure_mock.reset_mock()

        presto_coordinator.start(self.mock_env)
        assert configure_mock.called

    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    @patch('package.scripts.presto_coordinator.create_tpch_connector')
    def test_configure_adds_tpch_connector(self, create_tpch_connector_mock):
        presto_coordinator = Coordinator()
        open_mock = mock_open()

        with patch('__builtin__.open', open_mock):
            presto_coordinator.configure(self.mock_env)

        assert create_tpch_connector_mock.called

    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    @patch('package.scripts.presto_coordinator.smoketest_presto')
    @patch('package.scripts.presto_coordinator.Coordinator.configure')
    @patch('package.scripts.presto_coordinator.Execute')
    def test_start_smoketests_presto(
            self, execute_mock, unused_configure_mock, smoketest_presto_mock):
        presto_coordinator = Coordinator()

        presto_coordinator.start(self.mock_env)

        assert smoketest_presto_mock.called

    @patch('package.scripts.presto_coordinator.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_assert_constant_properties(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_coordinator = Coordinator()

        with patch('__builtin__.open', open_mock):
            presto_coordinator.configure(self.mock_env)

        assert 'discovery-server.enabled=true\n' in config
        assert 'coordinator=true\n' in config

    @patch('package.scripts.presto_coordinator.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_empty_queue_config_file(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_coordinator = Coordinator()

        with patch('__builtin__.open', open_mock):
            presto_coordinator.configure(self.mock_env)

        for item in config:
            assert not item.startswith('query.queue-config-file')

    @patch('package.scripts.presto_coordinator.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_pseudo_distributed(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_coordinator = Coordinator()

        with patch('__builtin__.open', open_mock):
            presto_coordinator.configure(self.mock_env)

        assert 'node-scheduler.include-coordinator=true\n' in config
