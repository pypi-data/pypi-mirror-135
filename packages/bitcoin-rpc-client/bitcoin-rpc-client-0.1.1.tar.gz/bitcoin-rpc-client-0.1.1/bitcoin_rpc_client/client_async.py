import itertools
import logging
import decimal
import json
from functools import partial
import httpx

from .error import JSONRPCError


class RPCClientAsync(object):
    def __init__(self, url, rpcuser, rpcpassword, parse_float=decimal.Decimal):
        self._next_id = itertools.count(1).__next__
        self.url = url
        self.rpcuser = rpcuser
        self.rpcpassword = rpcpassword
        self.parse_float = parse_float

        self._request = httpx.AsyncClient(auth=(rpcuser, rpcpassword))

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._request.aclose()

    async def aclose(self):
        await self._request.aclose()

    def __getattr__(self, name):
        return partial(self.call, name)

    async def call(self, method, *params):
        _id = self._next_id()

        logging.debug(
            "calling command {} with params {}".format(method, params))

        response = self._request.post(
            url=self.url,
            content=json.dumps(
                {
                    "jsonrpc": "2.0",
                    "id": _id,
                    "method": method,
                    "params": params,
                }
            ).encode('utf-8'))
        content = (await response).read().decode('utf-8')
        logging.debug("got response from daemon: " + content)
        resp = json.loads(content, parse_float=self.parse_float)

        if "error" in resp and resp["error"] is not None:
            raise JSONRPCError(resp["error"]["code"], resp["error"]["message"])

        if "result" not in resp:
            raise JSONRPCError(-343, "missing JSON-RPC result")

        return resp["result"]
