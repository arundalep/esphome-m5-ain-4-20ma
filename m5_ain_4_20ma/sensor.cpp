#include "m5_ain_4_20ma.h"
#include "esphome/core/log.h"

namespace esphome {
namespace m5_ain_4_20ma {

static const char *const TAG = "m5_ain_4_20ma";

void M5AIN4_20MASensor::setup() {
  ESP_LOGI(TAG, "Setting up M5Stack AIN 4-20mA sensor");
  ESP_LOGI(TAG, "I2C Address: 0x%02X", this->address_);
  ESP_LOGI(TAG, "Scaling Factor: %.4f", this->scaling_factor_);
}

void M5AIN4_20MASensor::dump_config() {
  LOG_SENSOR("", "M5 AIN 4-20mA", this);
  ESP_LOGCONFIG(TAG, "  I2C Address: 0x%02X", this->address_);
  ESP_LOGCONFIG(TAG, "  Scaling Factor: %.4f", this->scaling_factor_);
}

void M5AIN4_20MASensor::update() {
  // Read current value from register 0x20 (current value register)
  uint8_t data[2];
  
  ESP_LOGV(TAG, "Reading from I2C address 0x%02X", this->address_);
  
  // Write register address
  if (!this->write_bytes(0x20, nullptr, 0)) {
    ESP_LOGW(TAG, "Failed to write register address");
    this->publish_state(NAN);
    return;
  }
  
  // Read 2 bytes (little-endian)
  if (!this->read_bytes(0x20, data, 2)) {
    ESP_LOGW(TAG, "Failed to read data from device at 0x%02X", this->address_);
    this->publish_state(NAN);
    return;
  }
  
  // Combine bytes (little-endian: LSB first)
  uint16_t raw_value = (uint16_t)data[0] | ((uint16_t)data[1] << 8);
  
  ESP_LOGV(TAG, "Raw value: %u (0x%02X 0x%02X)", raw_value, data[0], data[1]);
  
  // Convert to mA using scaling factor
  float current_ma = raw_value * this->scaling_factor_;
  
  ESP_LOGV(TAG, "Current: %.4f mA", current_ma);
  
  // Sanity check for reasonable 4-20mA range
  if (current_ma < 0.0 || current_ma > 30.0) {
    ESP_LOGW(TAG, "Unusual current reading: %.4f mA (raw: %u)", current_ma, raw_value);
    ESP_LOGW(TAG, "You may need to adjust the scaling factor");
    // Still publish the value but log a warning
  }
  
  // Publish the sensor state
  this->publish_state(current_ma);
}

// Setter methods
void M5AIN4_20MASensor::set_address(uint8_t address) {
  this->address_ = address;
}

void M5AIN4_20MASensor::set_scaling_factor(float scaling_factor) {
  this->scaling_factor_ = scaling_factor;
}

}  // namespace m5_ain_4_20ma
}  // namespace esphome