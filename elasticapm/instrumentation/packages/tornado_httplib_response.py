from elasticapm.instrumentation.packages.base import AbstractInstrumentedModule
from elasticapm.traces import capture_span
from elasticapm.utils import default_ports
from elasticapm.utils.compat import urlparse


def get_host_from_url(url):
    parsed_url = urlparse.urlparse(url)
    host = parsed_url.hostname or " "

    if parsed_url.port and default_ports.get(parsed_url.scheme) != parsed_url.port:
        host += ":" + str(parsed_url.port)

    return host


class HttpClientTornadoInstrumentation(AbstractInstrumentedModule):
    name = "tornado"

    instrument_list = [("tornado.httpclient", "HTTPResponse")]

    def call(self, module, method, wrapped, instance, args, kwargs):
        http_request_proxy = args[0]
        url = http_request_proxy.url
        duration = kwargs.get('request_time', 0)
        signature = "async {} {}".format(http_request_proxy.method.upper(), get_host_from_url(http_request_proxy.url))
        with capture_span(signature, "ext.http.tornado", {"url": url}, leaf=True, async_process=True,
                          duration=duration):
            return wrapped(*args, **kwargs)
