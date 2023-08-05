import logging
import board
import adafruit_bh1750
from threading import Thread
from time import sleep


class LightSensor:

    def __init__(self):
        i2c = board.I2C()
        self.sensor = adafruit_bh1750.BH1750(i2c)
        logging.info("light sensor connected")

    def listen(self, listener):
        Thread(target=self.__listen, args=(listener,), daemon=True).start()

    def __listen(self, listener):
        while True:
            listener(self.sensor.lux)
            sleep(1)
