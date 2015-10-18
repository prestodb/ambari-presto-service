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

from package.scripts.presto_worker import Worker


class TestWorker(unittest.TestCase):

    dummy_config_properties = {'pseudo.distributed.enabled': 'true',
                               'query.queue-config-file': '',
                               'http-server.http.port': '8081',
                               'task.max-memory': '1GB'}

    def setUp(self):
        self.mock_env = MagicMock()

    @patch('package.scripts.presto_worker.Worker.configure')
    @patch('package.scripts.presto_worker.Execute')
    def test_lifecycle_methods_shell_out_to_execute(
            self, execute_mock, unused_configure_mock):
        presto_worker = Worker()

        presto_worker.install(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_worker.stop(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_worker.start(self.mock_env)
        assert execute_mock.called
        execute_mock.reset_mock()

        presto_worker.status(self.mock_env)
        assert execute_mock.called

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

    @patch('package.scripts.presto_worker.create_tpch_connector')
    def test_configure_adds_tpch_connector(self, create_tpch_connector_mock):
         presto_worker = Worker()

         with patch('__builtin__.open'):
            presto_worker.configure(self.mock_env)

         assert create_tpch_connector_mock.called

    @patch('package.scripts.presto_worker.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_pseudo_distribute_enabled_property(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_worker = Worker()

        with patch('__builtin__.open', open_mock):
            presto_worker.configure(self.mock_env)

        assert 'pseudo.distributed.enabled=true\n' not in config

    @patch('package.scripts.presto_worker.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_configure_ignore_empty_queue_config_file(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_worker = Worker()

        with patch('__builtin__.open', open_mock):
            presto_worker.configure(self.mock_env)

        for item in config:
            assert not item.startswith('query.queue-config-file')

    @patch('package.scripts.presto_worker.create_tpch_connector')
    @patch('package.scripts.params.config_properties', new=dummy_config_properties)
    def test_config_properties_coordinator_always_false(self, create_tpch_connector_mock):
        config = []
        open_mock = mock_file_descriptor_write_method(config)
        presto_worker = Worker()

        with patch('__builtin__.open', open_mock):
            presto_worker.configure(self.mock_env)

        assert 'coordinator=false\n' in config


def mock_file_descriptor_write_method(list):
    def append(item_to_append):
        list.append(item_to_append)

    open_mock = mock_open()
    fd = open_mock()
    fd.write = append
    return open_mock
