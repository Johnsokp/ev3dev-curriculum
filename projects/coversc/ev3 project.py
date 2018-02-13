import robot_controller as robo
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

class DataContainer(object):

    def __init__(self):
        self.running = True

    def drive_to_color(self, color_to_seek):
        print("Received: {} {}".format(color_to_seek))

        while robot.color_sensor.color != color_to_seek:
            robot.forward(100, 100)
            print(robot.color_sensor.color)
        robot.stop()

def main():
    robot = robo.Snatch3r()
    dc = DataContainer()

    ev3_delegate = DataContainer()
    mqtt_client = com.MqttClient(ev3_delegate)
    mqtt_client.connect_to_pc()

    print("--------------------------------------------")
    print("Let's run errands")
    print("--------------------------------------------")
    ev3.Sound.speak("Let's run errands").wait()

    while dc.running:
        btn.process()
        time.sleep(0.01)


main()
