import robot_controller as robo
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

class EV3(object):

    def __init__(self, r):
        self.running = True
        self.rrr = r
        self.speed = 450

    def drive_to_color(self, color_to_seek):

        print("Received: {}".format(color_to_seek))

        if color_to_seek == 'blue':
            color_number = 2
        elif color_to_seek == 'green':
            color_number = 6
        elif color_to_seek == 'red':
            color_number = 5

        while self.rrr.color_sensor.color != color_number:
            self.rrr.forward(200, 200)
            print(self.rrr.color_sensor.color)
        print('stop')

        if color_number == 2:
            self.rrr.forward(30, self.speed)
            self.rrr.turn_degrees(-90, self.speed)
            self.rrr.drive_inches(18, self.speed)
            self.rrr.arm_up()
            self.rrr.arm_down()
            self.rrr.drive_inches(-10, self.speed)
            # added code
            self.rrr.turn_degrees(176, self.speed)
            self.rrr.drive_inches(8, self.speed)
            self.rrr.turn_degrees(90, self.speed)
            self.rrr.seek_beacon()
            self.rrr.drive_inches(-12, self.speed)
            self.rrr.turn_degrees(180, self.speed)
            self.mqtt_client.send_message("message",['Where next?'])
        elif color_number == 3:
            self.rrr.turn_degrees(90, self.speed)
            self.rrr.drive_inches(24, self.speed)
            ev3.Sound.speak("We're learning today").wait()
            #added code
            self.rrr.turn_degrees(180, self.speed)
            self.rrr.drive_inches(24, self.speed)
            self.rrr.turn_degrees(-90, self.speed)
            self.rrr.seek_beacon()
            self.rrr.drive_inches(-5, self.speed)
            self.rrr.turn_degrees(180, self.speed)
            self.mqtt_client.send_message("message",['Where next?'])
        elif color_number == 5:
            self.rrr.turn_degrees(90, self.speed)
            self.rrr.drive_inches(20,  self.speed)
            self.rrr.turn_degrees(430, self.speed)
            ev3.Sound.speak('Home for the night!').wait()
            self.mqtt_client.send_message("message",['Home Sweet Home'])

    def go_home(self):
        self.rrr.seek_beacon()

    def set_speed(self, speed):
        self.speed = speed

def main():
    robot = robo.Snatch3r()
    #dc = EV3(robot)

    #new code
    #my_delegate = dc

    #mqtt_client = com.MqttClient(dc)
    #mqtt_client.connect_to_pc()

    my_delegate = EV3(robot)
    mqtt_client = com.MqttClient(my_delegate)
    my_delegate.mqtt_client = mqtt_client
    mqtt_client.connect_to_pc()


    print("--------------------------------------------")
    print("Let's run errands")
    print("--------------------------------------------")
    ev3.Sound.speak("Let's run errands").wait()

    robot.loop_forever()

    #robot.loop_forever()

main()
