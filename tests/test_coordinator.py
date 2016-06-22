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

from mock import MagicMock, patch, mock_open, call
from unittest import TestCase

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from package.scripts.presto_coordinator import Coordinator
from package.scripts.params import memory_configs
from test_worker import mock_file_descriptor_write_method, \
    collect_config_vars_written_out


class TestCoordinator(unittest.TestCase):

    dummy_config_properties = {'query.queue-config-file': '',
                               'http-server.http.port': '8285',
                               'node-scheduler.include-coordinator': 'true'}

    for memory_config in memory_configs:
        dummy_config_properties[memory_config] = '123'

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
        assert execute_mock.call_count is 2
        assert 'wget' in execute_mock.call_args_list[0][0][0]
        assert 'rpm -i' in execute_mock.call_args_list[1][0][0]
        assert 'export JAVA8_HOME=' in execute_mock.call_args_list[1][0][0]
        execute_mock.reset_mock()

        presto_coordinator.stop(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'stop' in execute_mock.call_args_list[0][0][0]
        execute_mock.reset_mock()

        presto_coordinator.start(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'start' in execute_mock.call_args_list[0][0][0]
        execute_mock.reset_mock()

        presto_coordinator.status(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'status' in execute_mock.call_args_list[0][0][0]

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

    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_adds_tpch_connector(self, create_connectors_mock):
        presto_coordinator = Coordinator()
        open_mock = mock_open()

        with patch('__builtin__.open', open_mock):
            presto_coordinator.configure(self.mock_env)

        assert call({}, "{'tpch': ['connector.name=tpch']}") in create_connectors_mock.call_args_list


    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    @patch('package.scripts.presto_coordinator.smoketest_presto')
    @patch('package.scripts.presto_coordinator.Coordinator.configure')
    @patch('package.scripts.presto_coordinator.Execute')
    def test_start_smoketests_presto(
            self, execute_mock, unused_configure_mock, smoketest_presto_mock, create_connectors_mock):
        presto_coordinator = Coordinator()

        presto_coordinator.start(self.mock_env)

        assert smoketest_presto_mock.called

    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new={})
    def test_assert_constant_properties(self, create_connectors_mock):
        config = collect_config_vars_written_out(self.mock_env, Coordinator())

        assert 'discovery-server.enabled=true\n' in config
        assert 'coordinator=true\n' in config
        assert 'node.data-dir=/var/lib/presto\n'

    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_empty_queue_config_file(self, create_connectors_mock):
        config = collect_config_vars_written_out(self.mock_env, Coordinator())

        for item in config:
            assert not item.startswith('query.queue-config-file')

    @patch('package.scripts.params.host_info', new={'presto_coordinator_hosts': ['master']})
    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_pseudo_distributed(self, create_connectors_mock):
        config = collect_config_vars_written_out(self.mock_env, Coordinator())

        assert 'node-scheduler.include-coordinator=true\n' in config

    @patch('package.scripts.presto_coordinator.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_memory_settings_have_units(self, create_connectos_mock):
        config = collect_config_vars_written_out(self.mock_env, Coordinator())

        assert_memory_configs_properly_formatted(config)

def assert_memory_configs_properly_formatted(configs_to_test):
    import re
    from package.scripts.params import memory_configs

    for memory_config in memory_configs:
        result = [x for x in configs_to_test \
                  if re.match(memory_config + '=\d*GB\n', x)]
        assert len(result) == 1
