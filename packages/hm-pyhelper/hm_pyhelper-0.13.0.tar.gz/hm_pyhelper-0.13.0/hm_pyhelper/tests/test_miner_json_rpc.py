import unittest
import mock
import responses
import requests
from hm_pyhelper.miner_json_rpc import MinerClient
from hm_pyhelper.miner_json_rpc.exceptions import MinerRegionUnset
from hm_pyhelper.miner_json_rpc.exceptions import MinerMalformedURL
from hm_pyhelper.miner_json_rpc.exceptions import MinerConnectionError

BASE_URL = 'http://helium-miner:4467'


@responses.activate
def response_result(data, status):
    url = "https://fake_url"
    responses.add(responses.POST, url, json=data, status=status)
    resp = requests.post(url)
    print(resp.json())
    return resp


def return_payload_with_method(method):
    return {'jsonrpc': '2.0', 'id': 1, 'method': method}


class Result(object):
    def __init__(self, result={'my': 'data'}):
        self.result = result


class Response(object):
    def __init__(self, data=Result()):
        self.data = data


class TestMinerJSONRPC(unittest.TestCase):
    def test_instantiation(self):
        client = MinerClient()
        self.assertIsInstance(client, MinerClient)
        self.assertEqual(client.url, BASE_URL)

    def test_malformed_url(self):
        client = MinerClient(url='fakeurl')

        exception_raised = False
        exception_type = None
        try:
            client.get_height()
        except Exception as exc:
            exception_raised = True
            exception_type = exc

        self.assertTrue(exception_raised)
        self.assertIsInstance(exception_type, MinerMalformedURL)

    def test_connection_error(self):
        client = MinerClient(url='http://notarealminer:9999')

        exception_raised = False
        exception_type = None
        try:
            client.get_height()
        except Exception as exc:
            exception_raised = True
            exception_type = exc

        self.assertTrue(exception_raised)
        self.assertIsInstance(exception_type, MinerConnectionError)

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    {"result": {'epoch': 25612, 'height': 993640}, "id": 1},
                    200))
    def test_get_height(self, mock_json_rpc_client):
        client = MinerClient()
        result = client.get_height()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('info_height'))

        self.assertEqual(result, {'epoch': 25612, 'height': 993640})

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    {"result": {'region': None}, "id": 1}, 200))
    def test_get_region_not_asserted(self, mock_json_rpc_client):
        client = MinerClient()
        exception_raised = False
        exception_type = None

        try:
            client.get_region()
        except Exception as exc:
            exception_raised = True
            exception_type = exc

        self.assertTrue(exception_raised)
        self.assertIsInstance(exception_type, MinerRegionUnset)

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    {"result": {'region': "EU868"}, "id": 1}, 200))
    def test_get_region(self, mock_json_rpc_client):
        client = MinerClient()
        result = client.get_region()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('info_region')
        )
        self.assertEqual(result, {'region': 'EU868'})

    summary = {
        'block_age': 1136610,
        'epoch': 25612,
        'firmware_version': "0.1",
        'gateway_details': 'undefined',
        'height': 993640,
        'mac_addresses': [
            {'eth0': '0242AC110002'},
            {'ip6tnl0': '00000000000000000000000000000000'},
            {'tunl0': '00000000'},
            {'lo': '000000000000'}
        ],
        'name': 'scruffy-chocolate-shell',
        'peer_book_entry_count': 3,
        'sync_height': 993640,
        'uptime': 144,
        'version': 10010005
    }

    result_json = {"result": summary, "id": 1}

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(result_json, 200))
    def test_get_summary(self, mock_json_rpc_client):
        client = MinerClient()
        result = client.get_summary()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('info_summary')
        )
        self.assertEqual(result, self.summary)

    peer_addr = '/p2p/11jr2kMp1bZvSC6pd3XkNvs9Q43qCgEzxRwV6vpuqXanC5UcLEs'

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    {"result": {'peer_addr': peer_addr}, "id": 1}, 200))
    def test_get_peer_addr(self, mock_json_rpc_client):

        client = MinerClient()
        result = client.get_peer_addr()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('peer_addr')
        )
        self.assertEqual(result, {'peer_addr': self.peer_addr})

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    {"result": [], "id": 1},
                    200))
    def test_get_peer_book(self, mock_json_rpc_client):

        client = MinerClient()
        result = client.get_peer_book()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('peer_book')
        )
        self.assertEqual(result, [])

    firmware_version = '2021.10.18.0'
    data_response = {
        'block_age': 1136610,
        'epoch': 25612,
        'firmware_version': firmware_version,
        'gateway_details': 'undefined',
        'height': 993640,
        'mac_addresses': [
            {'eth0': '0242AC110002'},
            {'ip6tnl0': '00000000000000000000000000000000'},
            {'tunl0': '00000000'},
            {'lo': '000000000000'}
        ],
        'name': 'scruffy-chocolate-shell',
        'peer_book_entry_count': 3,
        'sync_height': 993640,
        'uptime': 144,
        'version': 10010005
    }

    result_response = {"result": data_response, "id": 1}

    @mock.patch('hm_pyhelper.miner_json_rpc.client.requests.post',
                return_value=response_result(
                    result_response, 200))
    def test_get_firmware_version(self, mock_json_rpc_client):
        client = MinerClient()
        result = client.get_firmware_version()
        mock_json_rpc_client.assert_called_with(
            BASE_URL, json=return_payload_with_method('info_summary')
        )
        self.assertEqual(result, self.firmware_version)
