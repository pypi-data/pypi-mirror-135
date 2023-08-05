import itertools
import logging
import decimal
import json
from functools import partial
from urllib import request

from .error import JSONRPCError


class RPCClient(object):
    def __init__(self, url, rpcuser, rpcpassword, parse_float=decimal.Decimal):
        self._next_id = itertools.count(1).__next__
        self.url = url
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.parse_float = parse_float
        pw_mgr = request.HTTPPasswordMgrWithDefaultRealm()
        pw_mgr.add_password(None, url, user=rpcuser, passwd=rpcpassword)
        auth_handler = request.HTTPBasicAuthHandler(pw_mgr)
        self._request = request.build_opener(auth_handler)

    def __enter__(self):
        return self

    def __exit__(self, exc_type,exc_val,exc_tb):
        self._request.close()

    def __getattr__(self, name):
        return partial(self.call, name)

    def call(self, method, *params):
        _id = self._next_id()

        logging.debug(
            "calling command {} with params {}".format(method, params))

        req = request.Request(self.url, data=json.dumps({
            "jsonrpc": "2.0", "id": _id, "method": method, "params": params
        }).encode('utf-8'))
        
        with self._request.open(req) as response:
            content = response.read().decode('utf-8')
            logging.debug("got response from daemon: " + content)
            resp = json.loads(content, parse_float=self.parse_float)

            if "error" in resp and resp["error"] is not None:
                raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

            if "result" not in resp:
                raise JSONRPCError(-343, "missing JSON-RPC result")

            return resp["result"]

