# Phyto

Code for my hexapod plant pot robot named Phyto.

Phyto will periodically walk around, looking for a well-lit area to sit in.
When it finds a well-lit area, it will sit down for a while, and let its plant
soak in some sunlight.

## Hardware
- 1x [FREENOVE Big Hexapod Robot Kit](https://www.amazon.com/dp/B08M5DXS2P)
- 1x [Seeed Studio XIAO RP2040 microcontroller](https://www.seeedstudio.com/XIAO-RP2040-v1-0-p-5026.html)
- 4x [IMREN 30QP 18650 3000mAh 15A batteries](https://www.imrbatteries.com/imren-30qp-18650-3000mah-15a-battery/)

The hexapod kit includes a servo controller board, which is intended to be
controlled by a Raspberry Pi. Instead, I am using a Seeed Studio XIAO RP2040
microcontroller, because this is just a simple walking plant pot, and using a
whole Raspberry Pi would be too overpowered.

I used the FREENOVE Big Hexapod Robot Kit [software repository](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi)
to determine how the servos are controlled. Specifically, the
[Servo.py](https://github.com/Freenove/Freenove_Big_Hexapod_Robot_Kit_for_Raspberry_Pi/blob/master/Code/Server/Servo.py)
file shows the servo controller board uses two [PCA9685](https://www.nxp.com/docs/en/data-sheet/PCA9685.pdf)
16-channel PWM ICs to control the servos. They share an I2C bus, with addresses `0x40` and `0x41`.

The XIAO is connected to the servo controller board's 5V and GND pins for power,
and the SDA and SCL pins for I2C communication. The XIAO is also connected to
several directional light sensors to help Phyto seek out well-lit areas.

## Software

The XIAO RP2040 is running [CircuitPython](https://circuitpython.org/) with the
following libraries in the `lib` directory, copied from the
[Adafruit CircuitPython Bundle](https://github.com/adafruit/Adafruit_CircuitPython_Bundle):
- adafruit_motor
- adafruit_pca9685
  - adafruit_bus_device
  - adafruit_register

On startup, the XIAO runs the `code.py` script.
