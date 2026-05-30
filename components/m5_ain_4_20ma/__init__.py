"""ESPHome external component for M5Stack AIN 4-20mA unit

This component provides a sensor platform to read 4-20mA current values
from the M5Stack Unit AIN 4-20mA (SKU: U162) via I2C.

I2C Address: 0x55
Current Register: 0x20 (2 bytes, little-endian)
"""

import esphome.codegen as cg
from esphome.components import i2c

DEPENDENCIES = ["i2c"]

# Namespace for the component
m5_ain_4_20ma_ns = cg.esphome_ns.namespace("m5_ain_4_20ma")
M5AIN4_20MASensor = m5_ain_4_20ma_ns.class_(
    "M5AIN4_20MASensor", cg.PollingComponent, i2c.I2CDevice
)
