"""ESPHome external component for M5Stack AIN 4-20mA unit

This component provides a sensor platform to read 4-20mA current values
from the M5Stack Unit AIN 4-20mA (SKU: U162) via I2C.

I2C Address: 0x55
Current Register: 0x20 (2 bytes, little-endian)
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome import pins
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ADDRESS,
    CONF_ID,
    CONF_I2C_ID,
    CONF_UPDATE_INTERVAL,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    ICON_CURRENT_AC,
)

CODEOWNERS = ["@arundalep"]

DEPENDENCIES = ["i2c"]

CONF_M5_AIN_4_20MA = "m5_ain_4_20ma"
CONF_SCALING_FACTOR = "scaling_factor"

# Namespace for the component
m5_ain_4_20ma_ns = cg.esphome_ns.namespace("m5_ain_4_20ma")
M5AIN4_20MASensor = m5_ain_4_20ma_ns.class_(
    "M5AIN4_20MASensor", cg.PollingComponent, sensor.Sensor, i2c.I2CDevice
)

# Configuration schema
CONFIG_SCHEMA = (
    sensor.sensor_schema(
        M5AIN4_20MASensor,
        unit_of_measurement=UNIT_AMPERE,
        icon=ICON_CURRENT_AC,
        accuracy_decimals=2,
        state_class=STATE_CLASS_MEASUREMENT,
    )
    .extend(
        {
            cv.GenerateID(): cv.declare_id(M5AIN4_20MASensor),
            cv.Optional(CONF_I2C_ID): cv.use_id(i2c.I2CBus),
            cv.Optional(CONF_ADDRESS, default=0x55): cv.i2c_address,
            cv.Optional(
                CONF_SCALING_FACTOR, default=0.01
            ): cv.float_range(min=0.0001, max=100.0),
        }
    )
    .extend(i2c.i2c_device_schema(0x55))
    .extend(cv.COMPONENT_SCHEMA)
)

# Configuration validation and code generation
async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    await i2c.register_i2c_device(var, config)

    # Set the I2C address
    cg.add(var.set_address(config[CONF_ADDRESS]))
    
    # Set the scaling factor
    cg.add(var.set_scaling_factor(config[CONF_SCALING_FACTOR]))
    
    # Set update interval
    if CONF_UPDATE_INTERVAL in config:
        cg.add(var.set_update_interval(config[CONF_UPDATE_INTERVAL]))