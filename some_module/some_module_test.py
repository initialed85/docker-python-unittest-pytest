import json
import unittest

from mock import patch, Mock, call
from requests import Session, Response, ReadTimeout

from .some_module import SomeClass, GetIPAddressError

_TEST_IP_ADDRESS_JSON = """{"ip":"66.42.111.104","ip_decimal":1110077288,"country":"United States","country_eu":false,"country_iso":"US","city":"Los Angeles","hostname":"66.42.111.104.vultr.com","latitude":34.0729,"longitude":-118.2606}"""

_TEST_IP_ADDRESS_DICT = json.loads(_TEST_IP_ADDRESS_JSON)


class SomeClassTest(unittest.TestCase):
    def setUp(self):
        self.subject = SomeClass('Fred')

    #
    # these tests are simple black box style tests (testing the object without any contrived
    # behaviours)
    #

    def test_add_numbers_nominal(self):
        self.assertEqual(
            self.subject.add_numbers(8, 16),  # method to call (with args)
            'Hi Fred, 8 + 16 = 24'  # expected result
        )

    def test_add_numbers_boundary(self):
        self.assertEqual(
            self.subject.add_numbers(1000000000, 1000000000.137),  # method to call (with args)
            'Hi Fred, 1000000000 + 1000000000.137 = 2000000000.137'  # expected result
        )

    def test_add_numbers_erroneous(self):
        self.assertRaises(
            TypeError,  # expected result
            self.subject.add_numbers,  # method to call
            *('apples', 'oranges'),  # args to call it with
        )

    #
    # these tests replace the Session() constructor with a mock so we can contrive values
    # (because we can't rely on a HTTP request to a real service always returning the same
    # value)
    #

    @patch('requests.Session')
    def test_get_ip_address_nominal(self, mock_session_constructor):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 200
        mock_response.json.return_value = _TEST_IP_ADDRESS_DICT

        mock_session = Mock(spec=Session)
        mock_session.get.return_value = mock_response

        mock_session_constructor.return_value = mock_session

        self.assertEqual(
            self.subject.get_ip_address(),
            '66.42.111.104'
        )

        # check calls against the constructor
        self.assertEqual(
            mock_session_constructor.mock_calls,
            [
                call(),  # construction
                call().get('http://ifconfig.co/json'),
                call().get().json()
            ]
        )

        # check calls against the object the constructor returns
        self.assertEqual(
            mock_session.mock_calls,
            [
                call.get('http://ifconfig.co/json'),
                call.get().json()
            ]
        )

    @patch('requests.Session')
    def test_get_ip_address_boundary(self, mock_session_constructor):
        mock_response = Mock(spec=Response)
        mock_response.status_code = 403

        mock_session = Mock(spec=Session)

        mock_session_constructor.return_value = mock_session

        self.assertRaises(
            GetIPAddressError,
            self.subject.get_ip_address,  # method to call
        )

        # check calls against the constructor
        self.assertEqual(
            mock_session_constructor.mock_calls,
            [
                call(),  # construction
                call().get('http://ifconfig.co/json'),
                # note: no .json() call
            ]
        )

        # check calls against the object the constructor returns
        self.assertEqual(
            mock_session.mock_calls,  # check the calls against this object
            [
                call.get('http://ifconfig.co/json'),
                # note: no .json() call
            ]
        )

    @patch('requests.Session')
    def test_get_ip_address_erroneous(self, mock_session_constructor):
        mock_session = Mock(spec=Session)
        mock_session.get.side_effect = ReadTimeout('connection timed out')

        mock_session_constructor.return_value = mock_session

        self.assertRaises(
            ReadTimeout,
            self.subject.get_ip_address,  # method to call
        )

        # check calls against the constructor
        self.assertEqual(
            mock_session_constructor.mock_calls,
            [
                call(),  # construction
                call().get('http://ifconfig.co/json'),
                # note: no .json() call
            ]
        )

        # check calls against the object the constructor returns
        self.assertEqual(
            mock_session.mock_calls,  # check the calls against this object
            [
                call.get('http://ifconfig.co/json'),
                # note: no .json() call
            ]
        )
