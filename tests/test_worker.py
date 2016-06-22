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

import unittest
import os
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from package.scripts.presto_worker import Worker
from package.scripts.params import memory_configs


class TestWorker(unittest.TestCase):

    dummy_config_properties = {'pseudo.distributed.enabled': False,
                               'query.queue-config-file': '',
                               'http-server.http.port': '8285',
                               'node-scheduler.include-coordinator': False}

    minimal_config_properties = {'pseudo.distributed.enabled': False,
                                 'node-scheduler.include-coordinator': False}

    for memory_config in memory_configs:
        dummy_config_properties[memory_config] = '123'

    def setUp(self):
        self.mock_env = MagicMock()

    @patch('package.scripts.presto_worker.Worker.configure')
    @patch('package.scripts.presto_worker.Execute')
    def test_lifecycle_methods_shell_out_to_execute(
            self, execute_mock, unused_configure_mock):
        presto_worker = Worker()

        presto_worker.install(self.mock_env)
        assert execute_mock.call_count is 2
        assert 'wget' in execute_mock.call_args_list[0][0][0]
        assert 'rpm -i' in execute_mock.call_args_list[1][0][0]
        assert 'export JAVA8_HOME=' in execute_mock.call_args_list[1][0][0]
        execute_mock.reset_mock()

        presto_worker.stop(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'stop' in execute_mock.call_args_list[0][0][0]
        execute_mock.reset_mock()

        presto_worker.start(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'start' in execute_mock.call_args_list[0][0][0]
        execute_mock.reset_mock()

        presto_worker.status(self.mock_env)
        assert execute_mock.call_count is 1
        assert 'status' in execute_mock.call_args_list[0][0][0]

    @patch('package.scripts.presto_worker.Worker.configure')
    @patch('package.scripts.presto_worker.Execute')
    def test_install_start_configure_presto(
            self, unused_execute_mock, configure_mock):
        presto_worker = Worker()

        presto_worker.install(self.mock_env)
        assert configure_mock.called
        configure_mock.reset_mock()

        presto_worker.start(self.mock_env)
        assert configure_mock.called

    @patch('package.scripts.presto_worker.create_connectors')
    def test_configure_adds_tpch_connector(self, create_connectors_mock):
        presto_worker = Worker()

        with patch('__builtin__.open'):
            presto_worker.configure(self.mock_env)

        assert call({}, "{'tpch': ['connector.name=tpch']}") in create_connectors_mock.call_args_list

    @patch('package.scripts.presto_worker.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_pseudo_distribute_enabled_property(self, create_connectors_mock ):
        config = collect_config_vars_written_out(self.mock_env, Worker())

        assert 'pseudo.distributed.enabled=true\n' not in config

    @patch('package.scripts.presto_worker.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_empty_queue_config_file(self, create_connectors_mock):
        config = collect_config_vars_written_out(self.mock_env, Worker())

        for item in config:
            assert not item.startswith('query.queue-config-file')

    @patch('package.scripts.presto_worker.create_connectors')
    @patch('package.scripts.params.config_properties', new=minimal_config_properties)
    def test_constant_properties(self, create_connectors_mock):
        config = collect_config_vars_written_out(self.mock_env, Worker())

        assert 'coordinator=false\n' in config
        assert 'node.data-dir=/var/lib/presto\n' in config

    @patch('package.scripts.presto_worker.create_connectors')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_memory_settings_have_units(self, create_connectors_mock):
        from test_coordinator import assert_memory_configs_properly_formatted

        config = collect_config_vars_written_out(self.mock_env, Worker())
        assert_memory_configs_properly_formatted(config)


def collect_config_vars_written_out(mock_env, obj_under_test):
    config = []
    open_mock = mock_file_descriptor_write_method(config)

    with patch('__builtin__.open', open_mock):
        getattr(obj_under_test, 'configure')(mock_env)

    return config

def mock_file_descriptor_write_method(list):
    def append(item_to_append):
        list.append(item_to_append)

    open_mock = mock_open()
    fd = open_mock()
    fd.write = append
    return open_mock
