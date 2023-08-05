#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket
import eth_booster as eth

#print(dir(eth))

print(eth.hello_v())

print(eth.mapped({0: "world!!!"}))
print(eth.mapped({0: 2}))

bs = eth.Socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
address = eth.CAddress()
bs.getaddrinfo(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP, "192.168.168.100", 50007, address, 0);
bs.connect(address)
print(bs.rcv_buffer_size, bs.reuse_addr, bs.send_buffer_size)

#help(bs)


def main():
    pass

if __name__ == '__main__':
    main()

