from webthing import (SingleThing, Property, Thing, Value, WebThingServer)
from pi_lightsensor_webthing.lightsensor import LightSensor
import logging
import tornado.ioloop


class LightSensorThing(Thing):

    # regarding capabilities refer https://iot.mozilla.org/schemas
    # there is also another schema registry http://iotschema.org/docs/full.html not used by webthing

    def __init__(self, description: str, light_sensor: LightSensor):
        Thing.__init__(
            self,
            'urn:dev:ops:illuminanceSensor-1',
            'Illuminance Sensor',
            ['MultiLevelSensor'],
            description
        )

        light_sensor.listen(self.on_measured)

        self.bright = Value(0)
        self.add_property(
            Property(self,
                     'brightness',
                     self.bright,
                     metadata={
                         '@type': 'BrightnessProperty',
                         'title': 'Brightness',
                         "type": "integer",
                         'unit': 'lux',
                         'description': '"The brightness level in lux',
                         'readOnly': True,
                     }))

        self.ioloop = tornado.ioloop.IOLoop.current()

    def on_measured(self, brightness: float):
        self.ioloop.add_callback(self.__update_brightness, brightness)

    def __update_brightness(self, brightness: float):
        self.bright.notify_of_external_update(int(brightness))


def run_server(port: int, description: str = ""):
    light_sensor = LightSensorThing(description, LightSensor())
    server = WebThingServer(SingleThing(light_sensor), port=port, disable_host_validation=True)
    try:
        logging.info('starting the server')
        server.start()
    except KeyboardInterrupt:
        logging.info('stopping the server')
        server.stop()
        logging.info('done')
