import utime
from machine import ADC


class SEN0114:
    """
    Micro Python driver for the SEN0114 Soil Moisture Sensor
    """

    def __init__(self, adc: ADC):
        self.adc = adc

    @property
    def moisture(self) -> float:
        """
        Read the soil moisture value
        """
        value = self.adc.read_u16()
        return value / 65535


if __name__ == "__main__":
    PIN_ADC_0 = 26
    adc = ADC(PIN_ADC_0)
    sensor = SEN0114(adc)

    while True:
        value = int(sensor.moisture * 100)
        print(f"Moisture: {value:03}")
        utime.sleep(1)
