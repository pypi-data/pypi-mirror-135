# -*- coding: utf-8 -*-
# Python compatibility:
from __future__ import absolute_import

# Setup tools:
import pkg_resources

# Standard library:
from functools import wraps

try:
    pkg_resources.get_distribution('simplejson')
except pkg_resources.DistributionNotFound:
    # Standard library:
    from json import dumps
else:
    # 3rd party:
    from simplejson import dumps


def returns_json(raw):
    """
    Decorate the given function to ...
    - convert the result to JSON, and
    - add the appropriate HTTP headers
    """
    @wraps(raw)
    def wrapped(self, **kwargs):
        dic = raw(self, **kwargs)
        txt = dumps(dic)
        context = self.context
        setHeader = context.REQUEST.RESPONSE.setHeader
        setHeader('Content-Type', 'application/json; charset=utf-8')
        setHeader('Content-Length', len(txt))
        return txt
    return wrapped
