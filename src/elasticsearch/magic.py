"""Elasticearch IPython magic."""
from __future__ import print_function

import os
import urllib.parse

from IPython.core.magic import Magics, magics_class, line_cell_magic
import requests


@magics_class
class ElasticsearchMagics(Magics):
    def __init__(self, **kwargs):
        self._base_url = 'http://localhost:9200/'
        super().__init__(**kwargs)

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value
        print('Using: {}'.format(self.base_url))

    @line_cell_magic
    def elasticsearch(self, line, cell=None):
        "elasticsearch line magic"
        cell_base_url = line if line else self.base_url

        if not cell:
            self.base_url = cell_base_url
        else:
            line1 = (cell + os.linesep).find(os.linesep)
            method, path = cell[:line1].split(None, 1)
            body = cell[line1:].strip()
            data = body if body else None

            session = requests.Session()
            return session.send(requests.Request(method=method,
                                                 url=urllib.parse.urljoin(cell_base_url, path),
                                                 data=data).prepare()).json()


def load_ipython_extension(ipy):
    ipy.register_magics(ElasticsearchMagics)
