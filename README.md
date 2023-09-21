# OpenEyeTap 02w

This is both an update to, and a new design for, the OpenEyeTap by Prof. Steve Mann.

### OpenEyeTap Links

- [Instructable: OpenEyeTap: 3D Printed & Programmable Smart Glass](https://www.instructables.com/OpenEyeTap-3D-Printed-Programmable-Smart-Glass/),
- [Instructable: Augmented Reality Eyeglass With Thermal Vision: Build Your Own Low-cost Raspberry Pi EyeTap](https://www.instructables.com/Augmented-Reality-Eyeglass-With-Thermal-Vision-Bui/),
- [openeyetap.com (currently defunct)](https://openeyetap.com/)


## Background

I've personally been interested in computers since I was a child, and wearables for almost as
long. I came across the OpenEyeTap project and thought it was fantastic, but I have to wear glasses and there
wasn't an included "case" for that. It was also based on the Raspberry Pi Zero, which is fine as a simple proof
of concept, but it's quite underpowered.

Since the OET project was paused, RPi has released the Zero 2, which has the power of a standard RPi 3 but a
formfactor almost exactly like the OG Zero. And there has also been a major change in the Raspberry Pi OS as to
how the cameras are handled in the background.

With this all in mind, I set out in the late 20-teens to take all my general "wearable computer" notes and
see what I could do with them when basing everything on the OpenEyeTap concept.


## Hardware

I've designed a version of the eyetap that is self-contained and can be strapped to a pair of glasses. It
connects via a short micro-hdmi cable to a HAU (Hardware Attached Underneath) board connected under a
Raspberry Pi Zero 2w.

The HAU board connects to the Raspberry Pi via spring pins on the back, a well as a camera connector. The spring
pins connect to power, ground, the USB +/-/OTC and TV Out ports. A mini-usb power-in jack with power protection is
included in the HAU board.

The OET-side board is a splitter for the various hardware bits, as well as providing buttons to accomodate the
user interface buttons that the OET uses and the brightness controls for the screen.

We're in the process of switching from Fusion 360 to FreeCad, cause $700USD is just too damned much. Picture and
files will be added to this repository as I finish them.


## Software

Currently this software is basically a button-handling class for the buttons on the OET device, connected to an
MCP23008 on the i2c bus included in the camera wiring.

Next steps will be implementing a basic HUD drawn on the framebuffer, then adding audio recording controls,
and finally adding the camera when I can polarize the screen out of the camera's view.


## System Setup & Prerequisites

As with most other Raspberry Pi-based projects, you'll want to enable your local settings with the raspi-config
command. For this project, we need the i2c interface enabled.

There are some settings that need to be configured manually in the /boot/config.txt file. For the buttons
you need to ensure that this line is included. It will allow the i2c on the csi & dsi busses to show up as i2c-10.

```
dtparam=i2c_vc=on
```

For the screen, the best way I've found to make it work is to include:

```
dtoverlay=vc4-fkms-v3d,composite=1
enable_tvout=1
```


## Contributing

I welcome people helping, but haven't yet figured out any formalized way of doing this.


## Authors

  - **Adam Scriven** - *Initial coder* -
    [Scriven42](https://github.com/Scriven42)
  - **Thea Sky Barnes** - *framebuffer lib from aer pitftmanager code* -
    [tsbarnes](https://github.com/tsbarnes)      
    - https://github.com/tsbarnes/pitftmanager/
  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)

See also the list of
[contributors](https://github.com/Scriven42/oet02w/contributors)
who participated in this project.


## Acknowledgments

  - [Dr. Prof. Steve Mann](https://www.eecg.utoronto.ca/~mann/), for all his groundbreaking work on wearable computers
  - Hat tip to anyone whose code is used
  - There have been far too many sites that offered inspiration over the years,but I will try and collect as many here as I can

