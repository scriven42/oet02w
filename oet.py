#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Code partially inspired from an mcp23017 github, but I forgot to note which urls.
#


import time
import smbus


# MCP23008 address setup
address_map = {
    0x00: 'IODIR',
    0x01: 'IPOL',
    0x02: 'GPINTEN',
    0x03: 'DEFVAL',
    0x04: 'INTCON',
    0x05: 'IOCON',
    0x06: 'GPPU',
    0x07: 'INTF',
    0x08: 'INTCAP',
    0x09: 'GPIO',
    0x0A: 'OLAT'
}
register_map = {value: key for key, value in iter(address_map.items())}
max_len      = max(len(key) for key in register_map)


# OET Setup
mcp1_bus         = 10
mcp1_addr        = 0x20
mcp1_num_buttons = 4
mcp1_button_map  = {
    0: 'UI_1',
    1: 'UI_2',
    2: 'BR-',
    3: 'BR+',
}


# Other variables
counter          = 0
sleep            = 0.01


# Initialize the bus
bus = smbus.SMBus(mcp1_bus)

# and enable all the pullups
bus.write_byte_data(mcp1_addr, register_map['GPPU'], 0xFF)


def print_mcp_values(pmv_bus, pmv_addr):
    print("-" * 20)
    for addr in address_map:
        value = pmv_bus.read_byte_data(pmv_addr, addr)
        print("%-*s = 0x%02X" % (max_len, address_map[addr], value))


try:
    while True:
#        print_mcp_values(bus, mcp1_addr)
        gpio = bus.read_byte_data(mcp1_addr, register_map['GPIO'])
        for x in range(mcp1_num_buttons):
#            print("bit = {}".format(1<<x))
            if not (gpio & (1<<x)):
                print("{} Button Pressed!".format(mcp1_button_map[x]))
        counter += 1
#        print("counter = %s" % counter)
        time.sleep(sleep)
except KeyboardInterrupt:
    print("Keyboard interrupt")

