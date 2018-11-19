import mock
import pytest

from elasticapm.contrib.tornado import TornadoApm
from tests.contrib.tornado import BaseTestClass

pytest.importorskip("tornado")  # isort:skip


class TestTornadoAPM(BaseTestClass):

    def test_app_tornado_invalid(self):
        with self.assertRaises(Exception):
            app = None
            TornadoApm(app)

    @mock.patch("elasticapm.base.Client.capture_message")
    def test_capture_message(self, mock_client):
        app = mock.MagicMock()
        apm_tornado = TornadoApm(app)
        message_error = "Error"
        apm_tornado.capture_message(message_error)
        self.assertTrue(mock_client.called)

    @mock.patch("elasticapm.base.Client.capture_exception")
    def test_capture_exception(self, mock_client):
        app = mock.MagicMock()
        apm_tornado = TornadoApm(app)
        apm_tornado.capture_exception()
        self.assertTrue(mock_client.called)
