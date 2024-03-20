import network
import urequests as requests
import utime
from config import PASSWORD, SSID, TOKEN
from lib import ahtx0, charlcd_pico, moisture_pico
from machine import ADC, I2C, PWM, Pin, deepsleep

# INFLUXDB SETTINGS
URL = "http://raspberrypi:8086"
ORG = "raspberrypi"
BUCKET = "plant_monitor"
DEVICE_ID = "ficus"

# SETTINGS
BACKLIGHT_LEVEL = 0.3  # 0.0 to 1.0
INTERVAL = 1  # min

# PINS
PIN_BACKLIGHT = 14
PIN_I2C_SDA = 16
PIN_I2C_SCL = 17
PIN_ADC = 26  # ADC0

# INPUTS
I2C_CH = 0
LCD_ADDR = 0x3E
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


def connect_wifi() -> network.WLAN:
    # Wifi connection
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    # Wait for connect or fail
    max_mait = 10
    while max_mait > 0:
        if wlan.status() < 0 or wlan.status() >= 3:
            break
        max_mait -= 1
        print("waiting for connection...")
        utime.sleep(1)

    # Handle connection error
    if wlan.status() != 3:
        raise RuntimeError("network connection failed")
    else:
        print("wifi connected")
        status = wlan.ifconfig()
        print(f"ip = {status[0]}")

    return wlan


def main():
    while True:
        try:
            # Get sensor values
            temp: float = min(temp_sensor.temperature, 99.99)
            hum: float = min(temp_sensor.relative_humidity, 99.99)
            moisture: int = min(int(soil_sensor.moisture * 100), 100)
            wetness = "DRY"
            if moisture > 50:
                wetness = "WET"

            # Display values
            print("\nTemperature: %0.2f C" % temp)
            print("Humidity: %0.2f %%" % hum)
            print(f"Moisture: {moisture:03}")

            oled.move(0, 0)
            oled.write(f"{temp:0.1f}C")
            oled.move(0, 1)
            oled.write(f"{hum:0.1f}%")
            oled.move(5, 0)
            oled.write(f"{wetness}")
            oled.move(5, 1)
            oled.write(f"{moisture:03}")

            # Send values to InfluxDB
            Pin(23, Pin.OUT).high()
            wlan = connect_wifi()

            target_url = f"{URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=s"
            headers = {
                "content-type": "text/plain; charset=utf-8",
                "Accept": "application/json",
                "Authorization": f"Token {TOKEN}",
            }
            data = f"plant_sensor,device_id={DEVICE_ID} temperature={float(temp)},humidity={float(hum)},moisture={int(moisture)}"
            print("sending...")
            r = requests.post(target_url, data=data, headers=headers)
            print(f"sent ({r.status_code} {r.text}), status = {str(wlan.status())}")
            r.close()
            wlan.disconnect()
            wlan.active(False)

        except Exception as e:
            print(f"error ({e})")

        Pin(23, Pin.OUT).low()
        backlight.duty_u16(int(0))
        deepsleep(INTERVAL * 60 * 1000)


if __name__ == "__main__":
    main()
