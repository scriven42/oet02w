#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#


import time,datetime
import logging
import configparser
import json

# --- OET Button handling
from oet_buttons import OET_Buttons
import queue

# --- Image creation
import cv2
import numpy as np
from PIL import Image

# --- OET Screen-alone handling
# --- This is only needed if a camera is not installed or is disabled in some other way,
# --- when using the camera, it handles the direct-to-screen drawing as part of it's preview
# --- process and we can just jump on that for our overlays
from pitftmanager.libs.framebuffer import Framebuffer

# --- used to get rpi host status
import subprocess


# --- Constants
RED_RGB                 = (255,0,0,255)
BLUE_RGB                = (0,0,255,255)
BLUE_BGR                = RED_RGB
RED_BGR                 = BLUE_RGB
TYRIAN_PURPLE_RGB       = (102, 2, 60, 255)
TYRIAN_PURPLE_BGR       = (60, 2, 102, 255)
GREEN                   = (0,255,0,255)
WHITE                   = (255, 255, 255, 255)
TS_COLOUR               = WHITE
TS_FONT                 = cv2.FONT_HERSHEY_SIMPLEX
TS_SCALE                = 2
TS_THICKNESS            = 2
TS_ORIGIN               = (230, 90)
PAST_STATUS_ORIGIN      = (120, 70)     # To the left of the timestamp
PAST_STATUS_RADIUS      = 30
CUR_STATUS_ORIGIN       = (185, 70)
CUR_STATUS_RADIUS       = 30
HEARTBEAT_ORIGIN        = (120, 130)    # To the left and underneath the timestamp
HEARTBEAT_RADIUS        = 30
RECORDING_STATUS_ORIGIN = (185, 130)
RECORDING_STATUS_RADIUS = 30
BUTTON_STATUS_COLOUR    = GREEN
BUTTON_STATUS_FONT      = cv2.FONT_HERSHEY_SIMPLEX
BUTTON_STATUS_SCALE     = 3
BUTTON_STATUS_THICKNESS = 2
BUTTON_STATUS_ORIGIN    = (400, 400)


# --- Load Config
config = configparser.ConfigParser()
config.read('oet.ini')


# --- Setup variables
img_w                  = 1900
img_h                  = 1080
#img_w                  = 720
#img_h                  = 480
sleep_time             = 1.0
if config.has_option('Default','sleep'):
    sleep_time         = float(config.get('Default','sleep_time'))

timestamp_format       = "%Y%m%d_%H%M%S.%f%z"
if config.has_option('Default','timestamp_format'):
    timestamp_format   = config.get('Default','timestamp_format')

timedisplay_format     = "%Y-%m-%d %H:%M:%S %z"
if config.has_option('Default','timedisplay_format'):
    timedisplay_format = config.get('Default','timedisplay_format')


# --- OET Variables
framebuffer_num        = 0
if config.has_option('OET','framebuffer_num'):
    framebuffer_num    = int(config.get('OET','framebuffer_num'))


# --- Setup some functions and logging
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

# --- Start button queue and setup button callbacks
input_queue = queue.Queue()
logprint("Button Queue started.")

def ui1_hold_callback():
    input_queue.put('UI_1_HR')
    logprint("UI_1 Button Held and Released!")

def ui2_hold_callback():
    input_queue.put('UI_1_HR')
    logprint("UI_2 Button Held and Released!")

def ui1_click_callback():
    input_queue.put('UI_1_C')
    logprint("UI_1 Button Clicked!")

def ui2_click_callback():
    input_queue.put('UI_1_C')
    logprint("UI_2 Button Clicked!")

def brm_hold_callback():
    logprint("BR- Button Held and Released!")

def brp_hold_callback():
    logprint("BR+ Button Held and Released!")

def brm_click_callback():
    logprint("BR- Button Clicked!")

def brp_click_callback():
    logprint("BR+ Button Clicked!")

def main():
    oet_args = {
        'button0_click_clbk': ui1_click_callback,
        'button1_click_clbk': ui2_click_callback,
        'button2_click_clbk': brm_click_callback,
        'button3_click_clbk': brp_click_callback,
        'button0_hold_clbk': ui1_hold_callback,
        'button1_hold_clbk': ui2_hold_callback,
        'button2_hold_clbk': brm_hold_callback,
        'button3_hold_clbk': brp_hold_callback
    }
    oet = OET_Buttons(**oet_args)
    oet.start_loop_thread()
    logprint('OET Button Loop Thread started')

    framebuffer = Framebuffer(framebuffer_num)
    framebuffer.start()
    framebuffer.blank()
    logprint("Framebuffer #{} initialized: {}".format(framebuffer_num, framebuffer))
    # --- NOTE: BGR Colour Mode!

    is_recording = False
    time_prev    = datetime.datetime.fromtimestamp(0)

    while True:
        # --- Create Transparent Overlay
        overlay_frame = np.full((img_h, img_w, 4), (0, 0, 0, 0), np.uint8)

        # --- Add time stamp
        cv2.putText(overlay_frame, str(get_timedisplay()), TS_ORIGIN, TS_FONT, TS_SCALE, TS_COLOUR, TS_THICKNESS)

        # --- Determine raspberry pi status
        pt = subprocess.Popen(['/usr/bin/vcgencmd', 'get_throttled'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        (res,err) = pt.communicate()
        res = res.decode().split("=")[1]
        res = res.rstrip("\n")
        if ((int(res,0) & 0x01) == 0x01):
            cur_status_colour = RED_BGR
        else:
            cur_status_colour = GREEN
        if ((int(res,0) & 0x50000) == 0x50000):
            past_status_colour = RED_BGR
        else:
            past_status_colour = GREEN

        # --- Put some status circles, current then past
        # --- green for good red for bad
        cv2.circle(overlay_frame, (CUR_STATUS_ORIGIN),  CUR_STATUS_RADIUS,  cur_status_colour,  -1)
        cv2.circle(overlay_frame, (PAST_STATUS_ORIGIN), PAST_STATUS_RADIUS, past_status_colour, -1)

        # --- add a heartbeat circle
        time_now = datetime.datetime.now()
        time_diff = time_now - time_prev
        if (time_diff >= datetime.timedelta(seconds = 1)):
            heartbeat = True
            time_prev = time_now
        else:
            heartbeat = False
        if (heartbeat):
            cv2.circle(overlay_frame, (HEARTBEAT_ORIGIN), HEARTBEAT_RADIUS, TYRIAN_PURPLE_BGR, -1)

        # --- If we're recording, add another marker
        if (is_recording):
            recording_status_colour = RED_BGR
            cv2.circle(overlay_frame, (RECORDING_STATUS_ORIGIN), RECORDING_STATUS_RADIUS, recording_status_colour, -1)

        # --- Check input queue
        input_key = ''
        if (input_queue.qsize() > 0):
            input_key = input_queue.get()
            command = ''

#            if input_key == 'UI_1_C':
#            elif input_key == 'UI_1_HR':
#            elif input_key == 'UI_2_C':
#            elif input_key == 'UI_2_HR':

            # --- Add push button status
            cv2.putText(overlay_frame, str(input_key), BUTTON_STATUS_ORIGIN, BUTTON_STATUS_FONT, BUTTON_STATUS_SCALE, BUTTON_STATUS_COLOUR, BUTTON_STATUS_THICKNESS)


        # --- Finally the display process!
        overlay_frame = cv2.flip(overlay_frame, 0)
        overlay_frame = cv2.cvtColor(overlay_frame, cv2.COLOR_BGR2RGB)
        overlay_frame = Image.fromarray(overlay_frame)
        framebuffer.show(overlay_frame.resize(framebuffer.size))
        time.sleep(sleep_time)
    print("End.")


if (__name__ == '__main__'):
    main()

