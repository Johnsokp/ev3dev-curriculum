import robot_controller as robo
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

class DataContainer(object):

    def __init__(self, r):
        self.running = True
        self.rrr = r

    def drive_to_color(self, color_to_seek):
        print("Received: {}".format(color_to_seek))

        if color_to_seek == 'blue':
            color_number = 2
        elif color_to_seek == 'green':
            color_number = 3
        elif color_to_seek == 'red':
            color_number = 5

        while self.rrr.color_sensor.color != color_number:
            self.rrr.forward(100, 100)
            print(self.rrr.color_sensor.color)
        print('stop')
        self.rrr.stop()

def main():
    robot = robo.Snatch3r()
    dc = DataContainer(robot)

    mqtt_client = com.MqttClient(dc)
    mqtt_client.connect_to_pc()

    print("--------------------------------------------")
    print("Let's run errands")
    print("--------------------------------------------")
    ev3.Sound.speak("Let's run errands").wait()

    robot.loop_forever()

main()
