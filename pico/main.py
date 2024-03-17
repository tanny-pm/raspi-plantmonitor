import ahtx0
import charlcd_pico
import moisture_pico
import utime
from machine import ADC, I2C, PWM, Pin

# PINS
PIN_BACKLIGHT = 10
PIN_I2C_SDA = 16
PIN_I2C_SCL = 17
PIN_ADC = 26  # ADC0

# SETTINGS
I2C_CH = 0
LCD_ADDR = 0x3E
BACKLIGHT_LEVEL = 0.3  # 0.0 to 1.0

# INPUTS
i2c = I2C(I2C_CH, scl=Pin(PIN_I2C_SCL), sda=Pin(PIN_I2C_SDA), freq=400_000)
adc = ADC(PIN_ADC)

# DEVICES
temp_sensor = ahtx0.AHT20(i2c)
soil_sensor = moisture_pico.SEN0114(adc)
oled = charlcd_pico.AQM0802_pico(i2c, LCD_ADDR)

# OLED SETTINGS
oled.set_cursol(0)
oled.set_blink(0)
backlight = PWM(Pin(PIN_BACKLIGHT))
backlight.freq(10000)
backlight.duty_u16(int(65535 * BACKLIGHT_LEVEL))


while True:
    print("\nTemperature: %0.2f C" % temp_sensor.temperature)
    print("Humidity: %0.2f %%" % temp_sensor.relative_humidity)
    moisture = int(soil_sensor.moisture * 100)
    wetness = "DRY"
    if moisture > 50:
        wetness = "WET"
    print(f"Moisture: {moisture:03}")

    oled.move(0, 0)
    oled.write(f"{temp_sensor.temperature:0.1f}C")
    oled.move(0, 1)
    oled.write(f"{temp_sensor.relative_humidity:0.1f}%")
    oled.move(5, 0)
    oled.write(f"{wetness}")
    oled.move(5, 1)
    oled.write(f"{moisture:03}")

    utime.sleep(5)
