#pragma once

#include "esphome/components/sensor/sensor.h"
#include "esphome/components/i2c/i2c.h"
#include "esphome/core/component.h"

namespace esphome {
namespace m5_ain_4_20ma {

class M5AIN4_20MASensor : public sensor::Sensor, public PollingComponent, public i2c::I2CDevice {
 public:
  void setup() override;
  void dump_config() override;
  void update() override;
  
  void set_address(uint8_t address);
  void set_scaling_factor(float scaling_factor);

 protected:
  uint8_t address_{0x55};
  float scaling_factor_{0.01f};
};

}  // namespace m5_ain_4_20ma
}  // namespace esphome