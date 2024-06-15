from requests.adapters import BaseAdapter
from requests import Response, codes
import errno
import os
import stat
import locale
import io

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


class TextAdapter(BaseAdapter):
    def __init__(self, set_content_length=True):
        super(TextAdapter, self).__init__()
        self._set_content_length = set_content_length

    def send(self, request, **kwargs):
        """Wraps a file, described in request, in a Response object.

        :param request: The PreparedRequest` being "sent".
        :returns: a Response object containing the file
        """

        # Check that the method makes sense. Only support GET
        if request.method not in ("GET", "HEAD"):
            raise ValueError("Invalid request method %s" % request.method)
        url = request.url
        e = url[(url.find('://') + 3):]
        resp = Response()
        resp.request = request
        resp_str = str(e).encode(locale.getpreferredencoding(False))
        raw = BytesIO(resp_str)
        resp.raw = raw
        if self._set_content_length:
                resp.headers["Content-Length"] = len(resp_str)

        # Add release_conn to the BytesIO object
        raw.release_conn = raw.close
        resp.status_code = codes.ok
        resp.url = url

        return resp

    def close(self):
        pass
