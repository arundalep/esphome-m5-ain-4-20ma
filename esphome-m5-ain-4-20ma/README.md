# ESPHome Component for M5Stack AIN 4-20mA Unit

![ESPHome](https://img.shields.io/badge/ESPHome-Custom%20Component-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Platform](https://img.shields.io/badge/Platform-ESP32-orange)

ESPHome external component for the M5Stack Unit AIN 4-20mA current loop sensor interface. This component allows you to read 4-20mA industrial sensors directly with ESPHome on ESP32 devices like the M5 Atom.

## Features

- ✅ Reads 4-20mA current loop sensors via I2C
- ✅ Compatible with M5Stack AIN 4-20mA Unit (SKU: U162)
- ✅ Configurable I2C address
- ✅ Adjustable scaling factor for calibration
- ✅ Automatic error handling and logging
- ✅ Works with pressure, temperature, level, and other 4-20mA sensors

## Hardware

- **M5Stack Unit AIN 4-20mA** (SKU: U162)
- **ESP32 Device** (M5 Atom Lite/Matrix/S3, or any ESP32 with I2C)
- **4-20mA Sensor** (pressure, temperature, level, flow, etc.)

## Installation

### 1. Clone or Download This Repository

```bash
git clone https://github.com/YOUR_USERNAME/esphome-m5-ain-4-20ma.git
```

Or download as ZIP and extract.

### 2. Use External Component in ESPHome

Add to your ESPHome configuration:

```yaml
esphome:
  name: your-device-name
  # ... other esphome config ...
  
  external_components:
    - source: github://YOUR_USERNAME/esphome-m5-ain-4-20ma
      refresh: 0s
      components: [ m5_ain_4_20ma ]
```

**Replace `YOUR_USERNAME` with your actual GitHub username!**

### 3. Configure I2C

```yaml
i2c:
  sda: 26  # For M5 Atom Lite/Matrix
  scl: 32  # For M5 Atom S3, use sda: 2, scl: 1
  scan: true
```

### 4. Add the Sensor

```yaml
sensor:
  - platform: m5_ain_4_20ma
    i2c_id: bus_a
    address: 0x55
    update_interval: 1s
    name: "4-20mA Current"
    unit_of_measurement: "mA"
    icon: "mdi:current-ac"
    accuracy_decimals: 2
    # Optional: Adjust scaling factor if readings are off
    # scaling_factor: 0.01
```

## Configuration Options

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `name` | string | Required | Friendly name for the sensor |
| `address` | hex | `0x55` | I2C address of the M5Stack AIN unit |
| `update_interval` | time | `1s` | Update interval for readings |
| `scaling_factor` | float | `0.01` | Factor to convert raw value to mA |
| `unit_of_measurement` | string | `mA` | Unit displayed in Home Assistant |
| `icon` | string | `mdi:current-ac` | Icon for the sensor |
| `accuracy_decimals` | int | `2` | Number of decimal places |

## Scaling Factor

The `scaling_factor` converts the raw I2C value to mA. If your readings are way off, try different values:

**Symptoms and Solutions:**

- Reading is ~400-4000mA → Try `scaling_factor: 0.001`
- Reading is ~0.4-4mA → Try `scaling_factor: 0.01` ✅ **Most common**
- Reading is ~40-400mA → Try `scaling_factor: 0.1`

**Tip:** Start with `0.01` and adjust based on your readings and a multimeter measurement.

## Complete Example

```yaml
esphome:
  name: m5-atom-ain
  platform: ESP32
  board: m5stack-atom
  
  external_components:
    - source: github://YOUR_USERNAME/esphome-m5-ain-4-20ma
      components: [ m5_ain_4_20ma ]

  logger:
    level: DEBUG

wifi:
  ssid: "YourWiFi"
  password: "YourPassword"

api:
  encryption:
    key: "YourEncryptionKey"

# I2C for M5 Atom Lite
i2c:
  sda: 26
  scl: 32
  id: bus_a

sensor:
  # WiFi signal
  - platform: wifi_signal
    name: "WiFi Signal"
    
  # M5 AIN 4-20mA sensor
  - platform: m5_ain_4_20ma
    i2c_id: bus_a
    address: 0x55
    update_interval: 1s
    id: ain_current
    name: "4-20mA Current"
    unit_of_measurement: "mA"
    icon: "mdi:current-ac"
    accuracy_decimals: 2
    scaling_factor: 0.01
    filters:
      - sliding_window_moving_average:
          window_size: 5
          send_every: 5

  # Calibrated sensor
  - platform: template
    name: "Calibrated Current"
    unit_of_measurement: "mA"
    lambda: |-
      float raw = id(ain_current).state;
      # Apply your calibration
      return (raw + 0.02) * 0.9975;  # Example values

  # Convert to tank percentage
  - platform: template
    name: "Tank Level"
    unit_of_measurement: "%"
    lambda: |-
      float current = id(calibrated_current).state;
      if (current <= 4.0) return 0.0;
      if (current >= 20.0) return 100.0;
      return ((current - 4.0) / 16.0) * 100.0;
```

## M5 Atom PinOut

| Device | SDA | SCL |
|--------|-----|-----|
| Atom Lite | GPIO 26 | GPIO 32 |
| Atom Matrix | GPIO 26 | GPIO 32 |
| Atom S3 | GPIO 2 | GPIO 1 |

Update your `i2c:` section accordingly.

## Calibration

### Quick Calibration

1. **Connect sensor** to the M5Stack AIN unit
2. **Apply minimum signal** (empty tank, no pressure, etc.)
3. **Measure actual current** with a multimeter
4. **Compare to ESPHome reading**
5. **Calculate offset**: `offset = actual - reading`
6. **Apply maximum signal** (full tank, full pressure)
7. **Measure actual current** with multimeter
8. **Calculate scaling**: `scaling = actual / reading`

### Apply Calibration in YAML

```yaml
sensor:
  - platform: template
    name: "Calibrated Current"
    lambda: |-
      float raw = id(ain_current).state;
      // Replace with your values
      float offset = 0.02;      // From step 5
      float scaling = 0.9975;   // From step 8
      return (raw + offset) * scaling;
```

## Troubleshooting

### "I2C device not detected"

**Causes:**
- Loose Grove cable connection
- Wrong I2C pins (check your device variant)
- AIN unit not powered
- Defective AIN unit or cable

**Solutions:**
1. Reseat the Grove cable
2. Verify pin configuration in YAML
3. Check that ESP32 is powered
4. Try a different Grove cable
5. Enable I2C scan:
   ```yaml
   i2c:
     scan: true
     scan_interval: 60s
   ```

### "Readings are 0 or unrealistic"

**Possible Issues:**
1. **Wrong scaling factor** - Try different values (0.001, 0.01, 0.1)
2. **Sensor not connected** - Check sensor wiring
3. **Jumper cap wrong position** - Check internal/external power
4. **Open circuit** - Measure resistance, should be ~200Ω

### "Readings are noisy"

**Add filtering:**
```yaml
filters:
  - sliding_window_moving_average:
      window_size: 5
      send_every: 5
  - debounce: 0.5s
```

## Wiring

### M5 Atom to AIN Unit

Use the Grove cable:
- **Black** → GND
- **Red** → 5V
- **Yellow** → SDA
- **White** → SCL

### 4-Wire Sensor (Active)

```
24V Supply ─── Sensor+ ───│
                        ├──► Current Loop (4-20mA)
24V Ground ─── Sensor- ───│
                        │
Sensor+ Sig ────────────┼──► AIN IN+
Sensor- Sig ────────────┼──► AIN IN-
```

Set jumper on **JP1** (internal power mode).

### 2-Wire Sensor (Passive)

```
24V Supply ──┬──► Sensor+ ───► AIN IN+
             │
24V Ground ──┼──► AIN IN- ───► Sensor-
             │
            Current flows: Supply → Sensor → IN+ → IN- → Supply-
```

Set jumper on **JP2** (external power mode).

## Technical Details

**I2C Address:** 0x55  
**Current Register:** 0x20 (2 bytes, little-endian)  
**Update Rate:** Up to 100 Hz (configurable)  
**Input Range:** 4-20 mA  
**Input Impedance:** ~200Ω  
**Operating Temp:** 0-40°C  

### I2C Protocol

The component reads register `0x20` which returns a 2-byte little-endian value representing the current in 0.01mA units (default scaling).

**Example:**
- Raw value: `400` → 4.00 mA
- Raw value: `2000` → 20.00 mA

## Supported Sensors

This component works with any standard 4-20mA current loop sensor:

- ✅ Pressure transducers
- ✅ Temperature sensors (PT100 with 4-20mA transmitter)
- ✅ Tank level sensors
- ✅ Flow meters
- ✅ pH sensors
- ✅ Proximity sensors
- ✅ Any industrial 4-20mA sensor

## Examples

### Tank Level Sensor

```yaml
sensor:
  - platform: template
    name: "Tank Level"
    unit_of_measurement: "%"
    lambda: |-
      float current = id(ain_current).state;
      if (current <= 4.0) return 0.0;
      if (current >= 20.0) return 100.0;
      return ((current - 4.0) / 16.0) * 100.0;
```

### Pressure Sensor (0-10 bar)

```yaml
sensor:
  - platform: template
    name: "Pressure"
    unit_of_measurement: "bar"
    lambda: |-
      float current = id(ain_current).state;
      float pct = ((current - 4.0) / 16.0) * 100.0;
      return pct * 0.1;  # 10 bar / 100%
```

### Temperature Sensor (0-100°C)

```yaml
sensor:
  - platform: template
    name: "Temperature"
    unit_of_measurement: "°C"
    lambda: |-
      float current = id(ain_current).state;
      float pct = ((current - 4.0) / 16.0) * 100.0;
      return pct;  # Direct mapping for 0-100°C range
```

## Home Assistant Integration

Once configured, the sensor automatically appears in Home Assistant. Create automations:

```yaml
automation:
  - alias: "Alert: Tank Level Low"
    trigger:
      - platform: numeric_state
        entity_id: sensor.tank_level
        below: 20
    action:
      - service: notify.mobile_app
        data:
          message: "Tank level is critically low!"
```

## FAQ

**Q: Can I use multiple 4-20mA sensors?**  
A: The M5Stack AIN unit is single-channel only. For multiple sensors, use multiple AIN units on different I2C addresses (not tested) or use a different multi-channel board.

**Q: What's the maximum cable length?**  
A: 4-20mA signals can travel 100+ meters. Use shielded cable for best results.

**Q: Do I need an external power supply?**  
A: It depends on your sensor. 4-wire sensors have their own power. 2-wire sensors need external 24V DC supply.

**Q: Why use this instead of ADC + resistor?**  
A: This provides better accuracy, isolation, and ease of use. The AIN unit handles voltage-to-current conversion and provides signal isolation.

## License

MIT License - feel free to use and modify as needed.

## Credits

- **M5Stack** - for the AIN 4-20mA Unit hardware
- **ESPHome** - for the awesome platform
- Arduino library analysis for I2C protocol details

## Contributing

Contributions welcome! Feel free to submit issues and pull requests.

## Support

- Check the logs: `esphome logs your-device`
- Ensure I2C scan detects address 0x55
- Verify wiring and jumper configuration
- Test with known 4-20mA signal source

## Links

- [M5Stack AIN 4-20mA Product Page](https://docs.m5stack.com/en/unit/AIN4-20mA%20Unit)
- [ESPHome Documentation](https://esphome.io)
- [ESPHome Custom Component Guide](https://esphome.io/components/custom.html)

---

**Made with ❤️ for ESPHome Home Automation**