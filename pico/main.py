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

# OPTION
BACKLIGHT_LEVEL = 0.3  # 0.0 to 1.0
INTERVAL = 1  # minutes

# PINS
PIN_BACKLIGHT = 14
PIN_I2C_SDA = 16
PIN_I2C_SCL = 17
PIN_ADC = 26  # ADC0

# BUS
I2C_CH = 0
LCD_ADDR = 0x3E
i2c = I2C(I2C_CH, scl=Pin(PIN_I2C_SCL), sda=Pin(PIN_I2C_SDA), freq=400_000)
adc = ADC(PIN_ADC)

# DEVICES
temp_sensor = ahtx0.AHT20(i2c)
soil_sensor = moisture_pico.SEN0114(adc)
oled = charlcd_pico.AQM0802_pico(i2c, LCD_ADDR)
backlight = PWM(Pin(PIN_BACKLIGHT))
backlight.freq(10000)


def init_oled():
    oled.set_cursol(0)
    oled.set_blink(0)
    backlight.duty_u16(int(65535 * BACKLIGHT_LEVEL))


def read_sensor_values() -> tuple[float, float, int]:
    temp: float = min(temp_sensor.temperature, 99.99)
    hum: float = min(temp_sensor.relative_humidity, 99.99)
    moisture: int = min(int(soil_sensor.moisture * 100), 100)
    return temp, hum, moisture


def display_values(temp, hum, moist, moist_level):
    oled.move(0, 0)
    oled.write(f"{temp:0.1f}C")
    oled.move(0, 1)
    oled.write(f"{hum:0.1f}%")
    oled.move(5, 0)
    oled.write(f"{moist_level}")
    oled.move(5, 1)
    oled.write(f"{moist:03}")


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


def post_values_to_influxdb(temp, hum, moist):
    target_url = f"{URL}/api/v2/write?org={ORG}&bucket={BUCKET}&precision=s"
    headers = {
        "content-type": "text/plain; charset=utf-8",
        "Accept": "application/json",
        "Authorization": f"Token {TOKEN}",
    }
    data = f"plant_sensor,device_id={DEVICE_ID} temperature={float(temp)},humidity={float(hum)},moisture={int(moist)}"
    print("sending...")
    r = requests.post(target_url, data=data, headers=headers)
    print(f"sent: {r.status_code} {r.text}")
    r.close()


def main():
    init_oled()

    try:
        # Read sensor values
        temp, hum, moist = read_sensor_values()
        moist_level = "WET" if moist > 50 else "DRY"

        # Display values
        print(f"\nTemperature: {temp:.2f} C")
        print(f"Humidity: {hum:.2f} %")
        print(f"Moisture: {moist:03}")
        display_values(temp, hum, moist, moist_level)

        # WiFi ON
        Pin(23, Pin.OUT).high()
        wlan = connect_wifi()

        # Send values to InfluxDB
        post_values_to_influxdb(temp, hum, moist)

        wlan.disconnect()
        wlan.active(False)

    except Exception as e:
        print(f"Error: {e}")
        oled.clear()
        oled.write(f"{e}")

    finally:
        Pin(23, Pin.OUT).low()
        backlight.duty_u16(0)
        deepsleep(INTERVAL * 60 * 1000)


if __name__ == "__main__":
    main()
