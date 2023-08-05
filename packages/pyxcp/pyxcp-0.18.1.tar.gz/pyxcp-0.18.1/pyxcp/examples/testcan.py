
from pyxcp.master import Master
from pyxcp.types import AddressGranularity, XcpResponseError, XcpTimeoutError

import pyxcp

import pyxcp.transport.candriver
from pyxcp.transport.candriver.pc_socketcan import SocketCAN


cfg = {
    "TRANSPORT": "CAN",
    "CAN_DRIVER": "SocketCAN",
    "CAN_USE_DEFAULT_LISTENER": True,
    "CHANNEL": "vcan0",
    "CAN_ID_MASTER": 2045,
    "CAN_ID_SLAVE": 2046,
    "MAX_DLC_REQUIRED": False,
    "CREATE_DAQ_TIMESTAMPS": False,
    "FD": False
}

master = Master("Can", cfg)

print(master.connect())
print(master.getCommModeInfo())

result = master.getId(0x01)
if int(result.mode) == 1:
    name = bytes(result.identification).decode("ascii")
else:
    if result.length:
        name = bytes(master.upload(result.length)).decode("ascii")
    else:
        name = "<unknown>"

print(name)

