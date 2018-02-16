import robot_controller as robo
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

class DataContainer(object):

    def __init__(self, r):
        self.running = True
        self.rrr = r
        self.speed = 450

    def drive_to_color(self, color_to_seek):

        while not self.rrr.touch_sensor.is_pressed:
            #time.sleep(0.1)

            print("Received: {}".format(color_to_seek))

            if color_to_seek == 'blue':
                color_number = 2
            elif color_to_seek == 'green':
                color_number = 3

            while self.rrr.color_sensor.color != color_number:
                self.rrr.forward(100, 100)
                print(self.rrr.color_sensor.color)
            print('stop')

            if color_number == 2:
                self.rrr.turn_degrees(-90, self.speed)
                self.rrr.drive_inches(24, self.speed)
                self.rrr.arm_up()
                self.rrr.arm_down()
            elif color_number == 3:
                self.rrr.turn_degrees(90, self.speed)
                self.rrr.drive_inches(36, self.speed)
                ev3.Sound.speak("We're learning today").wait()

        def go_home(self):
            self.rrr.seek_beacon()

        def set_speed(self, speed):
            self.speed = speed

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
