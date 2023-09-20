#
# Code partially inspired from an mcp23017 github, but I forgot to note which urls.
#


import time
import smbus
import configparser
import json
from threading import Thread


# Setup some functions and logging
def keystoint(x):
    return {int(k): v for k, v in x}


class OET_Buttons:

    # MCP23008 setup
    address_map  = {
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


    # OET Setup
    button_sleep            = 1.0
    if config.has_option('OET','button_sleep'):
        button_sleep        = float(config.get('OET','button_sleep'))


    hold_time               = 1.0
    if config.has_option('OET','hold_time'):
        hold_time           = float(config.get('OET','hold_time'))


    double_click_time       = hold_time / 2
    if config.has_option('OET','double_click_time'):
        double_click_time = float(config.get('OET','double_click_time'))


    mcp1_bus_num            = 10
    if config.has_option('OET','mcp1_bus_num'):
        mcp1_bus_num        = int(config.get('OET','mcp1_bus_num'))


    mcp1_addr               = 0x20
    if config.has_option('OET','mcp1_addr'):
        mcp1_addr         = int(config.get('OET','mcp1_addr'), base=16)


    mcp1_button_map         = {
        0: 'UI_1',
        1: 'UI_2',
        2: 'BR-',
        3: 'BR+',
    }
    if config.has_option('OET','mcp1_button_map'):
        mcp1_button_map     = json.loads(config.get('OET','mcp1_button_map'), object_pairs_hook=keystoint)
    mcp1_num_buttons        = len(mcp1_button_map)


    # Setup the button info dictionaries to track status
    buttons_pressed         = []
    mcp1_button_info        = {}
    for x in range(mcp1_num_buttons):
        mcp1_button_info[x] = {}


    def __init__(self):
        # Initialize the bus
        self.mcp1_bus = smbus.SMBus(self.mcp1_bus_num)
        print("Bus #{} initialized".format(self.mcp1_bus_num))

        # and enable all the pullups
        self.mcp1_bus.write_byte_data(self.mcp1_addr, self.register_map['GPPU'], 0xFF)
        print("Pull-up resistors enabled for all pins on bus {} at address {}".format(self.mcp1_bus_num,hex(self.mcp1_addr)))


    def process_loop(self):
        while True:
            output = ""
            chord_change = False
#            print_mcp_values(self.mcp1_bus, self.mcp1_addr)
            gpio = self.mcp1_bus.read_byte_data(self.mcp1_addr, self.register_map['GPIO'])
            for x in range(self.mcp1_num_buttons):
                temp = ""
#                print("bit = {}".format(1<<x))
                now = time.time()
                if not (gpio & (1<<x)):
                    if ('status' not in self.mcp1_button_info[x] or self.mcp1_button_info[x]['status'] != "Pressed"):
                        self.mcp1_button_info[x]['status'] = "Pressed"
                        self.mcp1_button_info[x]['time'] = now
                        temp = "{} Button Pressed! ".format(self.mcp1_button_map[x])
                        if self.mcp1_button_map[x] not in self.buttons_pressed:
                            self.buttons_pressed.append(self.mcp1_button_map[x])
                            chord_change = True
                else:
                    if ('status' in self.mcp1_button_info[x] and self.mcp1_button_info[x]['status'] == "Pressed"):
                        self.mcp1_button_info[x]['status'] = "Released"
                        length = now - self.mcp1_button_info[x]['time']
                        if length >= 1:
                            temp = "Call Hold callback for {} (time: {})".format(self.mcp1_button_map[x], length)
#                            temp = "{} Button Released, was held for {} ".format(self.mcp1_button_map[x], length)
                        else:
                            temp = "Call Click callback for {} (time: {})".format(self.mcp1_button_map[x], length)
#                            temp = "{} Button Clicked (took: {}) ".format(self.mcp1_button_map[x], length)
                        self.mcp1_button_info[x]['time'] = now
                        self.buttons_pressed.remove(self.mcp1_button_map[x])
                        chord_change = True
                    output = output + temp
            if (len(self.buttons_pressed) > 1 and chord_change):
                output = output + "Buttons Pressed: {}".format(self.buttons_pressed)
            if output:
                print(output)
            time.sleep(self.button_sleep)


    def start_loop_thread(self):
        self.button_thread = Thread(target=self.process_loop)
        self.button_thread.start()


    def stop_loop_thread(self):
        self.button_thread.join()


    def print_mcp_values(self, pmv_bus, pmv_addr):
        print("-" * 20)
        for addr in self.address_map:
            value = pmv_bus.read_byte_data(pmv_addr, addr)
            print("%-*s = 0x%02X" % (self.max_len, self.address_map[addr], value))
