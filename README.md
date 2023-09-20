# OpenEyeTap 02w

This is both an update to, and a new design for, the OpenEyeTap by Prof. Steve Mann.


## Background

I've personally been interested in computers since I was a child, and wearables for almost as
long. I came across the OpenEyeTap project
([Instructable: OpenEyeTap: 3D Printed & Programmable Smart Glass](https://www.instructables.com/OpenEyeTap-3D-Printed-Programmable-Smart-Glass/),
[Instructable: Augmented Reality Eyeglass With Thermal Vision: Build Your Own Low-cost Raspberry Pi EyeTap](https://www.instructables.com/Augmented-Reality-Eyeglass-With-Thermal-Vision-Bui/),
[Currently defunct openeyetap.com](https://openeyetap.com/))
and thought it was fantastic, but I have to wear glasses and there wasn't an included "case" for that. It was
also based on the Raspberry Pi Zero, which is fine as a simple proof of concept, but it's quite underpowered.

Since the OET project was paused, RPi has released the Zero 2, which has the power of a standard RPi 3 but a
formfactor almost exactly like the OG Zero. And there has also been a major change in the Raspberry Pi OS as to
how the cameras are handled in the background.

With this all in mind, I set out in the late 20-teens to take all my general "wearable computer" notes and
see what I could do with them when basing everything on the OpenEyeTap concept.


## Hardware

I've designed a version of the eyetap that is self-contained and can be strapped to a pair of glasses. It connects to a HAU (Hardware Attached Underneath) connected under a Raspberry Pi Zero 2w via a short micro-hdmi cable.

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


## Contributing

Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code
of conduct, and the process for submitting pull requests to us.


## Authors

  - **Adam Scriven** - *Initial coder* -
    [Scriven42](https://github.com/Scriven42)
  - **Billie Thompson** - *Provided README Template* -
    [PurpleBooth](https://github.com/PurpleBooth)

See also the list of
[contributors](https://github.com/Scriven42/oet02w/contributors)
who participated in this project.


## Acknowledgments

  - [Dr. Prof. Steve Mann](https://www.eecg.utoronto.ca/~mann/), for all his groundbreaking work on wearable computers
  - Hat tip to anyone whose code is used
  - There have been far too many sites that offered inspiration over the years,but I will try and collect as many here as I can

