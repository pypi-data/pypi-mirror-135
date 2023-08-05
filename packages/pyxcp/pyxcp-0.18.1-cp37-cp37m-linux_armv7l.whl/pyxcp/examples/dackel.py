#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Very basic hello-world example.
"""

__copyright__ = """
    pySART - Simplified AUTOSAR-Toolkit for Python.

   (C) 2009-2019 by Christoph Schueler <cpu12.gems@googlemail.com>

   All Rights Reserved

  This program is free software; you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation; either version 2 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License along
  with this program; if not, write to the Free Software Foundation, Inc.,
  51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
"""


import time
from pprint import pprint

from pyxcp.cmdline import ArgumentParser

ap = ArgumentParser(description = "pyXCP hello world.")
with ap.run() as x:
    x.connect()
    if x.slaveProperties.optionalCommMode:
        x.getCommModeInfo()
    gid = x.getId(0x1)
    result = x.fetch(gid.length)

    print("DAQ_PROC_INFO: ", x.getDaqProcessorInfo())
    print("TIMESTAMP: {:04X}".format(x.getDaqClock()))
    #print("readDAQ:", x.readDaq())
    print("daqResolutionInfo", x.getDaqResolutionInfo())
    dpi = x.getDaqProcessorInfo()
    #x.getDaqEventInfo(3)
    for ecn in range(dpi.maxEventChannel):
        eci = x.getDaqEventInfo(ecn)
        print(eci)
        data = x.upload(eci.eventChannelNameLength)
        print("EventChannelName:", data.decode("latin1"))
    x.setDaqListMode(0x10, 0, 1, 1, 0)
    x.startStopDaqList(2, 0)
    x.startStopSynch(1)
    time.sleep(5.0)
    print("\nSlave properties:")
    print("=================")
    print("ID: '{}'".format(result.decode("utf8")))
    pprint(x.slaveProperties)
    x.disconnect()
