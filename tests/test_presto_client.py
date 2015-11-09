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

import re
import socket
import os
import json
import sys
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from mock import MagicMock, patch, PropertyMock
from httplib import HTTPException, HTTPConnection
from unittest import TestCase

from package.scripts.presto_client import smoketest_presto, PrestoClient, \
    InvalidArgumentError, URL_TIMEOUT_MS

class TestPrestoClientSmoketest(TestCase):

    nation = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14,
              15, 16, 17, 18, 19, 20, 21, 22, 23, 24]

    def setUp(self):
        self.presto_client_mock = MagicMock()

    @patch('package.scripts.presto_client.time.sleep', return_value=None)
    def test_presto_queried_on_smoketest(self, unused_sleep_mock):
        self.presto_client_mock.get_rows.side_effect = [[['master']], 'dummy_val', TestPrestoClientSmoketest.nation]

        smoketest_presto(self.presto_client_mock, ['master'])

        assert self.presto_client_mock.execute_query.called

    @patch('package.scripts.presto_client.time.sleep', return_value=None)
    def test_failure_when_fewer_than_25_rows_returned_from_nation(self, unused_sleep_mock):
        self.presto_client_mock.get_rows.return_value = [['master']]

        TestCase.assertRaises(self, RuntimeError, smoketest_presto, self.presto_client_mock, ['master'])

    @patch('package.scripts.presto_client.ensure_nodes_are_up', side_effect=RuntimeError())
    def test_failure_when_nodes_are_not_up(self, ensure_nodes_are_up_mock):
        TestCase.assertRaises(self, RuntimeError, smoketest_presto, self.presto_client_mock, ['master'])

    @patch('package.scripts.presto_client.time.sleep', return_value=None)
    @patch('package.scripts.presto_client.ensure_catalogs_are_available', side_effect=RuntimeError())
    def test_failure_when_catalogs_are_not_available(self, ensure_catalogs_are_available_mock,
                                                     unused_sleep_mock):
        TestCase.assertRaises(self, RuntimeError, smoketest_presto, self.presto_client_mock, ['master'])

    @patch('package.scripts.presto_client.time.sleep', return_value=None)
    def test_failure_when_nodes_returned_dont_match_nodes_specified(self, unused_sleep_mock):
        self.presto_client_mock.get_rows.return_value = [['bad_host']]

        TestCase.assertRaises(self, RuntimeError, smoketest_presto, self.presto_client_mock, ['master'])

# These tests were copied more or less verbatim from
# https://github.com/prestodb/presto-admin/blob/master/tests/unit/test_prestoclient.py
class TestPrestoClient(TestCase):

    def test_no_sql(self):
        client = PrestoClient('any_host', 'any_user', 8080)
        self.assertRaisesRegexp(InvalidArgumentError,
                                'SQL query missing',
                                client.execute_query, '', )

    def test_no_server(self):
        client = PrestoClient('', 'any_user', 8080)
        self.assertRaisesRegexp(InvalidArgumentError,
                                'Server IP missing',
                                client.execute_query, 'any_sql')

    def test_no_user(self):
        client = PrestoClient('any_host', '', 8080)
        self.assertRaisesRegexp(InvalidArgumentError,
                                'Username missing',
                                client.execute_query, 'any_sql')

    @patch('package.scripts.presto_client.HTTPConnection')
    def test_default_request_called(self, mock_conn):
        client = PrestoClient('any_host', 'any_user', 8080)
        headers = {'X-Presto-Catalog': 'tpch', 'X-Presto-Schema': 'sf1',
                   'X-Presto-User': 'any_user'}

        client.execute_query('any_sql')
        mock_conn.assert_called_with('any_host', 8080, False, URL_TIMEOUT_MS)
        mock_conn().request.assert_called_with('POST', '/v1/statement',
                                               'any_sql', headers)
        self.assertTrue(mock_conn().getresponse.called)

    @patch('package.scripts.presto_client.HTTPConnection')
    def test_connection_failed(self, mock_conn):
        client = PrestoClient('any_host', 'any_user', 8080)
        client.execute_query('any_sql')

        self.assertTrue(mock_conn().close.called)
        self.assertFalse(client.execute_query('any_sql'))

    @patch('package.scripts.presto_client.HTTPConnection')
    def test_http_call_failed(self, mock_conn):
        client = PrestoClient('any_host', 'any_user', 8080)
        mock_conn.side_effect = HTTPException('Error')
        self.assertFalse(client.execute_query('any_sql'))

        mock_conn.side_effect = socket.error('Error')
        self.assertFalse(client.execute_query('any_sql'))

    @patch.object(HTTPConnection, 'request')
    @patch.object(HTTPConnection, 'getresponse')
    def test_http_answer_valid(self, mock_response, mock_request):
        client = PrestoClient('any_host', 'any_user', 8080)
        mock_response.return_value.read.return_value = '{}'
        type(mock_response.return_value).status = \
            PropertyMock(return_value=200)
        self.assertTrue(client.execute_query('any_sql'))

    @patch.object(HTTPConnection, 'request')
    @patch.object(HTTPConnection, 'getresponse')
    def test_http_answer_not_json(self, mock_response, mock_request):
        client = PrestoClient('any_host', 'any_user', 8080)
        mock_response.return_value.read.return_value = 'NOT JSON!'
        type(mock_response.return_value).status =\
            PropertyMock(return_value=200)
        self.assertRaisesRegexp(ValueError, 'No JSON object could be decoded',
                                client.execute_query, 'any_sql')

    @patch.object(PrestoClient, 'get_response_from')
    @patch.object(PrestoClient, 'get_next_uri')
    def test_retrieve_rows(self, mock_uri, mock_get_from_uri):
        client = PrestoClient('any_host', 'any_user', 8080)
        dir = os.path.abspath(os.path.dirname(__file__))

        with open(dir + '/resources/valid_rest_response_level1.txt') \
                as json_file:
            client.response_from_server = json.load(json_file)
        mock_get_from_uri.return_value = True
        mock_uri.side_effect = [
            "http://localhost:8080/v1/statement/2015_harih/2", ""
        ]

        self.assertEqual(client.get_rows(), [])
        self.assertEqual(client.next_uri,
                         "http://localhost:8080/v1/statement/2015_harih/2")

        with open(dir + '/resources/valid_rest_response_level2.txt') \
                as json_file:
            client.response_from_server = json.load(json_file)
        mock_uri.side_effect = [
            "http://localhost:8080/v1/statement/2015_harih/2", ""
        ]

        expected_row = [["uuid1", "http://localhost:8080", "presto-main:0.97",
                         True],
                        ["uuid2", "http://worker:8080", "presto-main:0.97",
                         False]]
        self.assertEqual(client.get_rows(), expected_row)
        self.assertEqual(client.next_uri, "")

    @patch.object(PrestoClient, 'get_response_from')
    @patch.object(PrestoClient, 'get_next_uri')
    def test_append_rows(self, mock_uri, mock_get_from_uri):
        client = PrestoClient('any_host', 'any_user', 8080)
        dir = os.path.abspath(os.path.dirname(__file__))

        with open(dir + '/resources/valid_rest_response_level2.txt') \
                as json_file:
            client.response_from_server = json.load(json_file)
        mock_get_from_uri.return_value = True
        mock_uri.side_effect = ["any_next_uri", "any_next_next_uri", "", ""]
        expected_row = [["uuid1", "http://localhost:8080", "presto-main:0.97",
                         True],
                        ["uuid2", "http://worker:8080", "presto-main:0.97",
                         False],
                        ["uuid1", "http://localhost:8080", "presto-main:0.97",
                         True],
                        ["uuid2", "http://worker:8080",  "presto-main:0.97",
                         False]]
        self.assertEqual(client.get_rows(), expected_row)

    @patch.object(PrestoClient, 'get_response_from')
    @patch.object(PrestoClient, 'get_next_uri')
    def test_limit_rows(self, mock_uri, mock_get_from_uri):
        client = PrestoClient('any_host', 'any_user', 8080)
        dir = os.path.abspath(os.path.dirname(__file__))
        with open(dir + '/resources/valid_rest_response_level2.txt') \
                as json_file:
            client.response_from_server = json.load(json_file)
        mock_get_from_uri.return_value = True
        mock_uri.side_effect = ["any_next_uri", ""]

        self.assertEqual(client.get_rows(0), [])

    @patch('package.scripts.presto_client.urlopen')
    @patch('httplib.HTTPResponse')
    def test_get_response(self, mock_resp, mock_urlopen):
        client = PrestoClient('any_host', 'any_user', 8080)
        mock_urlopen.return_value = mock_resp
        mock_resp.read.return_value = '{"message": "ok!"}'

        client.get_response_from('any_uri')
        self.assertEqual(client.response_from_server, {"message": "ok!"})

    # This method is equivalent to Python 2.7's unittest.assertRaisesRegexp()
    def assertRaisesRegexp(self, expected_exception, expected_regexp,
                           callable_object, *args, **kwargs):
        if 'msg' in kwargs and kwargs['msg']:
            msg = '\n' + kwargs['msg']
        else:
            msg = ''
        try:
            callable_object(*args)
        except expected_exception as e:
            self.assertTrue(re.search(expected_regexp, str(e)),
                            repr(expected_regexp) + ' not found in '
                            + repr(str(e)) + msg)
        else:
            self.fail('Expected exception ' + str(expected_exception) +
                      ' not raised' + msg)