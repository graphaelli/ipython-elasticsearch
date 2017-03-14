"""ElasticSearch IPython magic."""
from __future__ import absolute_import, print_function

import getpass
import json
import os
import urllib.parse

from IPython.core.magic import Magics, magics_class, line_cell_magic
import requests

from . import notebook as nb


@magics_class
class ElasticsearchMagics(Magics):
    def __init__(self, shell=None, **kwargs):
        self._base_url = 'http://localhost:9200/'
        self.user_name = self.password = None
        nb.output_notebook()
        super().__init__(shell=shell, **kwargs)
        self._store = {}

        # Define '_es', which is visible to the notebook user and can be used to
        # access ElasticSearch query results from other cells. For example, a
        # query cell that begins:
        #
        # %%elasticsearch
        # GET ecommerce_orders/_search :orders_by_country
        #
        # can be accessed from another cell with the following syntax:
        #
        # _es['orders_by_country']
        #
        # This was inspired by:
        # http://stackoverflow.com/questions/33508377/read-cell-content-in-an-ipython-notebook
        shell.user_ns['_es'] = self._store

    @property
    def base_url(self):
        return self._base_url

    @base_url.setter
    def base_url(self, value):
        self._base_url = value

        # Execute a test request against the server to verify access.
        rsp = self._es_request(self._base_url, '_search?size=0', 'GET', None)

        # If the request failed, ask for user name and password. We cache these
        # values so they are only requested once per notebook.
        while rsp.status_code == 401:
            print('Enter user name')
            self.user_name = getpass.getpass()
            print('Enter password')
            self.password = getpass.getpass()
            rsp = self._es_request(self._base_url, '_search', 'GET', None)

        print('Using: {}'.format(self.base_url))

    @line_cell_magic
    def elasticsearch(self, line, cell=None):
        "elasticsearch line magic"
        cell_base_url = line if line else self.base_url

        if not cell:
            self.base_url = cell_base_url
        else:
            line1 = (cell + os.linesep).find(os.linesep)
            line1_split = cell[:line1].split(None, 2)
            result_name = None
            # Optional third parameter is result name, e.g.
            # GET ecommerce_orders/_search :orders_by_country
            if len(line1_split) == 3:
                result_name = line1_split[2]
                if result_name.startswith(':'):
                    result_name = result_name[1:]
                line1_split = line1_split[:2]
            method, path = line1_split
            body = cell[line1:].strip()
            data = body if body else None

            rsp = self._es_request(cell_base_url, path, method, data)
            try:
                response_json = rsp.json()
                nb.output_cell(response_json)
                if result_name:
                    self._store[result_name] = response_json
            except json.JSONDecodeError:
                # TODO: parse charset out of response eg: 'application/json; charset=UTF-8'
                # >>> requests.get("http://localhost:9200/_search").headers['Content-Type']
                # 'application/json; charset=UTF-8'
                # >>> requests.get("http://localhost:9200/_cat").headers['Content-Type']
                # 'text/plain; charset=UTF-8'
                print(rsp.content.decode('UTF-8'))  # ES [probably] always returns utf-8
            return rsp

    def _es_request(self, base_url, path, method, data):
        session = requests.Session()
        rsp = session.send(requests.Request(
            method=method,
            url=urllib.parse.urljoin(base_url, path),
            data=data,
            auth=(self.user_name, self.password)
            if self.password else None).prepare())
        return rsp


def load_ipython_extension(ipy):
    ipy.register_magics(ElasticsearchMagics)
