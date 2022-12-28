import unittest
import urllib.error
import urllib.parse
import urllib.request
from unittest import mock

from ns_schedule import create_json, create_headers, retrieve_schedule, extract_arguments


class Unittests(unittest.TestCase):
    @mock.patch("os.environ", {'NS_APIKEY': 'Foo'})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_api_happy_flow(self):
        expected = {'Ocp-Apim-Subscription-Key': 'Foo'}
        self.assertEqual(expected, create_headers())

    @mock.patch("os.environ", {})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_no_api_key(self):
        expected = [{'title': 'Please specify API key in settings'}]
        self.assertEqual(expected, retrieve_schedule())

    def test_create_json(self):
        expected = '{"items": [{"title": "Title1", "subtitle": "Sub1", "arg": "http://example.com"}, ' \
                   '{"title": "Title2", "subtitle": "Sub2", "arg": "http://dummy.host"}]}'
        self.assertEqual(expected, create_json([{"title": "Title1", "subtitle": "Sub1", "arg": "http://example.com"},
                                                {"title": "Title2", "subtitle": "Sub2", "arg": "http://dummy.host"}]))

    @mock.patch("sys.argv", ["main"])
    def test_no_args(self):
        expected = [{'title': 'Please provide origin and destination stations'}]
        self.assertEqual(expected, retrieve_schedule())

    @mock.patch("sys.argv", ["main", "Foo"])
    def test_wrong_args(self):
        expected = [{"title": "Please provide origin and destination stations"}]
        self.assertEqual(expected, retrieve_schedule())

    @mock.patch("sys.argv", ["main", "Foo Bar Baz"])
    def test_too_many_args(self):
        expected = [{"title": "Please provide origin and destination stations"}]
        self.assertEqual(expected, retrieve_schedule())

    @mock.patch("os.environ", {'NS_APIKEY': 'Foo'})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_happyflow(self):
        with open('testdata/happyflow.json') as json_file:
            with mock.patch('urllib.request.urlopen') as urlopen_mock:
                mock_response = urlopen_mock.return_value
                mock_response.read.return_value = json_file.read()
                expected = [{
                    "arg": "https://www.ns.nl/dummy1",
                    "subtitle": "Track: 9b\t\t\tIntercity + Intercity",
                    "title": "22:01 -> 23:02\t\t\tDuration: (1:01)\tTransfers: 1x"}, {
                    "arg": "https://www.ns.nl/dummy2",
                    "subtitle": "Track: 2\t\t\tIntercity",
                    "title": "22:22 -> 23:05\t\t\tDuration: (0:43)\tTransfers: 0x"}, {
                    "arg": "https://www.ns.nl/dummy3",
                    "subtitle": "Track: 9b\t\t\tIntercity + Intercity",
                    "title": "22:31 -> 23:32\t\t\tDuration: (1:01)\tTransfers: 1x"}, {
                    "arg": "https://www.ns.nl/dummy4",
                    "subtitle": "Track: 1\t\t\tIntercity",
                    "title": "22:52 -> 23:35\t\t\tDuration: (0:43)\tTransfers: 0x"}]
                self.assertEqual(expected, retrieve_schedule())

    @mock.patch("os.environ", {'NS_APIKEY': 'Foo'})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_happyflow_cancelled(self):
        with open('testdata/cancelled.json') as json_file:
            with mock.patch('urllib.request.urlopen') as urlopen_mock:
                mock_response = urlopen_mock.return_value
                mock_response.read.return_value = json_file.read()
                expected = [{
                    "arg": "https://www.ns.nl/dummy1",
                    "subtitle": "CANCELLED\t\t\tIntercity + Intercity",
                    "title": "22:01 -> 23:02\t\t\tDuration: (1:01)\tTransfers: 1x"}, {
                    "arg": "https://www.ns.nl/dummy2",
                    "subtitle": "Track: 2\t\t\tIntercity",
                    "title": "22:22 -> 23:05\t\t\tDuration: (0:43)\tTransfers: 0x"}, {
                    "arg": "https://www.ns.nl/dummy3",
                    "subtitle": "Track: 9b\t\t\tIntercity + Intercity",
                    "title": "22:31 -> 23:32\t\t\tDuration: (1:01)\tTransfers: 1x"}, {
                    "arg": "https://www.ns.nl/dummy4",
                    "subtitle": "Track: 1\t\t\tIntercity",
                    "title": "22:52 -> 23:35\t\t\tDuration: (0:43)\tTransfers: 0x"}]
                self.assertEqual(expected, retrieve_schedule())

    @mock.patch("os.environ", {'NS_APIKEY': 'Foo'})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_malformed_json(self):
        with open('testdata/malformed.json') as json_file:
            with mock.patch('urllib.request.urlopen') as urlopen_mock:
                mock_response = urlopen_mock.return_value
                mock_response.read.return_value = json_file.read()
                expected = [{"title": "Can\'t parse server response"}]
                self.assertEqual(expected, retrieve_schedule())

    @mock.patch('urllib.request.urlopen')
    @mock.patch("os.environ", {'NS_APIKEY': 'Foo'})
    @mock.patch("sys.argv", ["main", "Foo Bar"])
    def test_bad_request(self, urlopen_mock):
        urlopen_mock.side_effect = urllib.error.HTTPError(*[None] * 5)
        expected = [{"title": "Error contacting server"}]
        self.assertEqual(expected, retrieve_schedule())

    @mock.patch("sys.argv", ["main", "Den_Haag_Centraal Amsterdam_Centraal"])
    def test_argument_parsing(self):
        expected = ["Den Haag Centraal", "Amsterdam Centraal"]
        self.assertEqual(extract_arguments(), expected)


if __name__ == '__main__':  # pragma: nocover
    unittest.main()
