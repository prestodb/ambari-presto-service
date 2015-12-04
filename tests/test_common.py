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
from unittest import TestCase
from mock import patch, call
import sys
import os
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from test_worker import mock_file_descriptor_write_method


class TestCommonCode(TestCase):
    node_properties = {'plugin.config-dir': '/does/not/exist'}

    @patch('package.scripts.common.Execute')
    def test_no_connectors_to_add(self, unused_execute_mock):
        from package.scripts.common import create_connectors

        connector_properties_written_out = collect_connector_properties_written_out(
            create_connectors, self.node_properties, '')

        assert not connector_properties_written_out


        connector_properties_written_out = collect_connector_properties_written_out(
            create_connectors, self.node_properties, '{}')

        assert not connector_properties_written_out

    @patch('package.scripts.common.Execute')
    def test_add_connector(self, unused_execute_mock):
        from package.scripts.common import create_connectors
        
        connector_properties = "{'hive': ['key1=value1', 'key2=value2']}"

        connector_properties_written_out = collect_connector_properties_written_out(
            create_connectors, self.node_properties, connector_properties)

        assert connector_properties_written_out == ['key1=value1\n', 'key2=value2\n']

    @patch('package.scripts.common.Execute')
    def test_no_connectors_to_delete(self, execute_mock):
        from package.scripts.common import delete_connectors

        delete_connectors(self.node_properties, '')

        assert not execute_mock.called

        delete_connectors(self.node_properties, '{}')

        assert not execute_mock.called

    @patch('package.scripts.common.Execute')
    def test_delete_connector(self, execute_mock):
        from package.scripts.common import delete_connectors

        delete_connectors(self.node_properties, "['connector1', 'connector2']")

        assert execute_mock.call_args_list == [call('rm -f /does/not/exist/connector1.properties'),
                                               call('rm -f /does/not/exist/connector2.properties')]

def collect_connector_properties_written_out(
        create_connectors_method, node_properties, connectors_properties):
    connector_properties_written_out = []
    open_mock = mock_file_descriptor_write_method(connector_properties_written_out)

    with patch('__builtin__.open', open_mock):
        create_connectors_method(node_properties, connectors_properties)

    return connector_properties_written_out