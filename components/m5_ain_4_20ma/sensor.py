"""M5Stack AIN 4-20mA Sensor Component

Platform integration for the M5Stack AIN 4-20mA sensor.
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import (
    CONF_ADDRESS,
    CONF_I2C_ID,
    CONF_ID,
    STATE_CLASS_MEASUREMENT,
    UNIT_AMPERE,
    ICON_CURRENT_AC,
)

from . import M5AIN4_20MASensor

CONF_SCALING_FACTOR = "scaling_factor"

# Configuration schema for the sensor platform
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
            cv.Optional(CONF_I2C_ID): cv.use_id(i2c.I2CBus),
            cv.Optional(CONF_ADDRESS, default=0x55): cv.i2c_address,
            cv.Optional(
                CONF_SCALING_FACTOR, default=0.01
            ): cv.float_range(min=0.0001, max=100.0),
        }
    )
    .extend(i2c.i2c_device_schema(0x55))
)


async def to_code(config):
    var = cg.new_Pvariable(config[CONF_ID])
    await cg.register_component(var, config)
    await sensor.register_sensor(var, config)
    await i2c.register_i2c_device(var, config)

    # Set the I2C address
    if CONF_ADDRESS in config:
        cg.add(var.set_address(config[CONF_ADDRESS]))
    
    # Set the scaling factor
    if CONF_SCALING_FACTOR in config:
        cg.add(var.set_scaling_factor(config[CONF_SCALING_FACTOR]))
