import pytest

pytest.importorskip("tornado")  # isort:skip

import mock
from elasticapm.contrib.tornado import ApiElasticHandlerAPM
from elasticapm.contrib.tornado import TornadoApm
import tornado


class MockMatcher:
    _path = "test/%s/extref/%s"
    regex = mock.MagicMock()


class MockWillCardRouter:
    target = ""
    matcher = MockMatcher()


def test_capture_exception():
    application = mock.MagicMock()
    request = mock.MagicMock()
    client = mock.MagicMock()
    application().settings.get.return_value = client
    handler = ApiElasticHandlerAPM(application, request)
    handler.capture_exception()
    assert application.called


def test_capture_message():
    application = mock.MagicMock()
    client = mock.MagicMock()
    application().settings.get.return_value = client
    request = mock.MagicMock()
    handler = ApiElasticHandlerAPM(application, request)
    message = "error"
    handler.capture_message(message)
    assert application.called


def test_write_error():
    application = mock.MagicMock()
    client = mock.MagicMock()
    application().settings.get.return_value = client
    request = mock.MagicMock()
    handler = ApiElasticHandlerAPM(application, request)
    handler.write_error(status_code=400)
    assert application.called


def test_prepare():
    application = mock.MagicMock()
    client = mock.MagicMock()
    application().settings.get.return_value = client
    request = mock.MagicMock()
    handler = ApiElasticHandlerAPM(application, request)
    handler.prepare()
    assert application.called


def test_get_url():
    application = mock.MagicMock()
    request = mock.MagicMock()
    handler = ApiElasticHandlerAPM(application, request)
    mock_will = MockWillCardRouter()
    mock_will.matcher.regex.groupindex.values.return_value = [1, 2]
    mock_will.matcher.regex.groupindex.items.return_value = [('operator', 1), ('extref', 2)]
    mock_will.target = handler.__class__
    application.wildcard_router.rules = [mock_will]
    url = handler.get_url()
    assert url == 'test/:operator/extref/:extref'


@mock.patch("elasticapm.contrib.tornado.elasticapm")
def test_on_finish(mock_elastic):
    application = mock.MagicMock()
    client = mock.MagicMock()
    application().settings.get.return_value = client
    request = mock.MagicMock()
    handler = ApiElasticHandlerAPM(application, request)
    handler.get_url = mock.Mock()
    handler.on_finish()
    assert application.called
    assert handler.get_url.called
    assert mock_elastic.set_context.called


def test_app_tornado_invalid():
    with pytest.raises(Exception):
        app = None
        TornadoApm(app)


@mock.patch("elasticapm.base.Client.capture_message")
def test_capture_message(mock_client):
    app = mock.MagicMock()
    apm_tornado = TornadoApm(app)
    message_error = "Error"
    apm_tornado.capture_message(message_error)
    assert mock_client.called


@mock.patch("elasticapm.base.Client.capture_exception")
def test_capture_exception(mock_client):
    app = mock.MagicMock()
    apm_tornado = TornadoApm(app)
    apm_tornado.capture_exception()
    assert mock_client.called

# class TestApiMcafee(BaseTestClassTornado):
#
#     def test_error_handler(self):
#         url = "/error"
#         response = self.fetch(url, method='GET')
#         print(response)
