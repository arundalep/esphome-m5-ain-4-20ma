"""Sensor platform for M5Stack AIN 4-20mA unit.

This component reads 4-20mA current values from the M5Stack Unit AIN
4-20mA (SKU: U162) via I2C.

I2C Address: 0x55
Current Register: 0x20 (2 bytes, little-endian)
"""

import esphome.codegen as cg
import esphome.config_validation as cv
from esphome.components import i2c, sensor
from esphome.const import CONF_ADDRESS

CONF_SCALING_FACTOR = "scaling_factor"

m5_ain_4_20ma_ns = cg.esphome_ns.namespace("m5_ain_4_20ma")
M5AIN4_20MASensor = m5_ain_4_20ma_ns.class_(
    "M5AIN4_20MASensor", cg.PollingComponent, sensor.Sensor, i2c.I2CDevice
)

CONFIG_SCHEMA = (
    sensor.sensor_schema(
        M5AIN4_20MASensor,
        unit_of_measurement="mA",
        icon="mdi:current-ac",
        accuracy_decimals=2,
        device_class="current",
        state_class="measurement",
    )
    .extend(
        {
            cv.Optional(CONF_SCALING_FACTOR, default=0.01): cv.float_range(
                min=0.0001, max=100.0
            ),
        }
    )
    .extend(cv.polling_component_schema("1s"))
    .extend(i2c.i2c_device_schema(0x55))
)


async def to_code(config):
    var = await sensor.new_sensor(config)
    await cg.register_component(var, config)
    await i2c.register_i2c_device(var, config)

    cg.add(var.set_address(config[CONF_ADDRESS]))
    cg.add(var.set_scaling_factor(config[CONF_SCALING_FACTOR]))
