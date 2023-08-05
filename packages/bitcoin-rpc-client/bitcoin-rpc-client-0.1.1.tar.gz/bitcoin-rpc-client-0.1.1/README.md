# Bitcoin RPC Client

RPC client for Bitcoin Daemons

## Install

```bash
pip install bitcoin-rpc-client
```

## Usage

Prerequesites:

Run a Bitcoin daemon/node
```bash
bitcoind -server -rpcuser=user -rpcpassword=pass
```

### Sync

```python
from bitcoin_rpc_client import RPCClient

with RPCClient('http://127.0.0.1:18443', 'user', 'pass') as rpc:
    blocks = rpc.generate(101)
    tx = rpc.sendtoaddress(address, 20)

# or 

rpc = RPCClient('http://127.0.0.1:18443', 'user', 'pass')
blocks = rpc.generate(101)
tx = rpc.sendtoaddress(address, 20)
rpc.close()
```

### Async

```python
from bitcoin_rpc_client import RPCClientAsync

with RPCClientAsync('http://127.0.0.1:18443', 'user', 'pass') as rpc:
    blocks = await rpc.generate(101)
    tx = await rpc.sendtoaddress(address, 20)

# or

rpc = RPCClientAsync('http://127.0.0.1:18443', 'user', 'pass')
blocks = await rpc.generate(101)
tx = await rpc.sendtoaddress(address, 20)
await rpc.aclose()
```