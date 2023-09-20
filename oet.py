#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Code partially inspired from an mcp23017 github, but I forgot to note which urls.
#


import time,datetime
import smbus
import logging
import configparser
import json


# MCP23008 setup
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

# Load Config
config = configparser.ConfigParser()
config.read('oet.ini')

# Other variables
counter               = 0
sleep                 = 1.0
if config.has_option('Default','sleep'):
    sleep             = float(config.get('Default','sleep'))

timestamp_format      = "%Y%m%d_%H%M%S"
if config.has_option('Default','timestamp_format'):
    timestamp_format  = config.get('Default','timestamp_format')

timedisplay_format    = "%Y-%m-%d %H:%M:%S"
if config.has_option('Default','timedisplay_format'):
    timedisplay_format = config.get('Default','timedisplay_format')


# Setup some functions and logging
def keystoint(x):
    return {int(k): v for k, v in x}


def get_timestamp():
    now = datetime.datetime.now()
    return str(now.strftime(timestamp_format))


def get_timedisplay():
    now = datetime.datetime.now()
    return str(now.strftime(timedisplay_format))


logging.basicConfig(filename='oet_'+get_timestamp()+'.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')
logging.debug('Logging started')


def logprint(lp_text):
    logging.info(lp_text)
    print(lp_text)


def print_mcp_values(pmv_bus, pmv_addr):
    print("-" * 20)
    for addr in address_map:
        value = pmv_bus.read_byte_data(pmv_addr, addr)
        print("%-*s = 0x%02X" % (max_len, address_map[addr], value))


# OET Setup
mcp1_bus_num        = 1
if config.has_option('OET','mcp1_bus_num'):
    mcp1_bus_num    = int(config.get('OET','mcp1_bus_num'))

mcp1_addr           = 0x20
if config.has_option('OET','mcp1_addr'):
    mcp1_addr       = int(config.get('OET','mcp1_addr'), base=16)

mcp1_button_map     = {
    0: 'UI_1',
    1: 'UI_2',
    2: 'UI_3',
    3: 'UI_4',
}
if config.has_option('OET','mcp1_button_map'):
    mcp1_button_map = json.loads(config.get('OET','mcp1_button_map'), object_pairs_hook=keystoint)

mcp1_num_buttons    = len(mcp1_button_map)
mcp1_button_info    = {}
for x in range(mcp1_num_buttons):
    mcp1_button_info[x] = {}


# Initialize the bus
mcp1_bus = smbus.SMBus(mcp1_bus_num)
logprint("Bus #{} initialized".format(mcp1_bus_num))

# and enable all the pullups
mcp1_bus.write_byte_data(mcp1_addr, register_map['GPPU'], 0xFF)
logprint("Pull-up resistors enabled for all pins on bus {} at address {}".format(mcp1_bus_num,hex(mcp1_addr)))


try:
    buttons_pressed = []
    while True:
        output = ""
        chord_change = False
#        print_mcp_values(mcp1_bus, mcp1_addr)
        gpio = mcp1_bus.read_byte_data(mcp1_addr, register_map['GPIO'])
        for x in range(mcp1_num_buttons):
            temp = ""
#            print("bit = {}".format(1<<x))
            if not (gpio & (1<<x)):
                if ('status' not in mcp1_button_info[x] or mcp1_button_info[x]['status'] != "Pressed"):
                    mcp1_button_info[x]['status'] = "Pressed"
                    mcp1_button_info[x]['time'] = time.time()
                    temp = "{} Button Pressed! ".format(mcp1_button_map[x])
                    if x not in buttons_pressed:
                        buttons_pressed.append(x)
                        chord_change = True
            else:
                if ('status' in mcp1_button_info[x] and mcp1_button_info[x]['status'] == "Pressed"):
                    mcp1_button_info[x]['status'] = "Released"
                    now = time.time()
                    length = now - mcp1_button_info[x]['time']
                    temp = "{} Button Released, was held for {} ".format(mcp1_button_map[x], length)
                    mcp1_button_info[x]['time'] = now
                    buttons_pressed.remove(x)
                    chord_change = True
            output = output + temp
        if (len(buttons_pressed) > 1 and chord_change):
            output = output + "Chords: {}".format(buttons_pressed)
        if output:
            logprint(output)
        counter += 1
#        print("counter = %s" % counter)
        time.sleep(sleep)
except KeyboardInterrupt:
    logprint("Keyboard interrupt")

