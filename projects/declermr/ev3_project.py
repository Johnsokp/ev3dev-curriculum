"""
This section serves as the base code running on the EV3. Its job is to make sure the EV3 is able to move according
to the input that is received. It also sends feedback regarding the status of the EV3 and its environment.

The EV3 is programmed to receive a signal from the computer to move around. This is done using the MQTT that it
and the computer uses as a communication device. The program ends
"""

import mqtt_remote_method_calls as com

import robot_controller as robo

import random


# class MyDelegate(object):
#
#     def __init__(self):
#         self.running = True
#
#     def set_led(self, led_side_string, led_color_string):
#         print("Received: {} {}".format(led_side_string, led_color_string))
#         led_side = None
#         if led_side_string == "left":
#             led_side = ev3.Leds.LEFT
#         elif led_side_string == "right":
#             led_side = ev3.Leds.RIGHT
#
#         led_color = None
#         if led_color_string == "green":
#             led_color = ev3.Leds.GREEN
#         elif led_color_string == "red":
#             led_color = ev3.Leds.RED
#         elif led_color_string == "black":
#             led_color = ev3.Leds.BLACK
#
#         if led_side is None or led_color is None:
#             print("Invalid parameters sent to set_led. led_side_string = {} led_color_string = {}".format(
#                 led_side_string, led_color_string))
#         else:
#             ev3.Leds.set_color(led_side, led_color)
#
#


def main():
    robot = robo.Snatch3r

    robo.ev3.Sound.speak("test test").wait()

    # canvas = 'Ev3_Led button'
    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_pc()

    # Buttons on EV3 (these obviously assume TO DO: 3. is done)
    btn = robo.ev3.Button()
    # btn.on_backspace = robot.shutdown()
    """
    Stretch goal: implement button functions for celebration
    """
    # btn.on_up = lambda state:
    # btn.on_down = lambda state:
    # btn.on_left = lambda state:
    # btn.on_right = lambda state:

    while robot.running:
        btn.process()
        print(1)
        review_touchdown(mqtt_client, robot, robo.ev3.ColorSensor.COLOR_BLUE)
        print(2)


# ----------------------------------------------------------------------
# Sense the color.
# ----------------------------------------------------------------------


def mud(mqtt_client, robot, color_to_seek, num_list):
    random_num = random.randrange(1, 100)
    num_list.append(random_num)
    while robot.color_sensor.color != color_to_seek:
        for k in range(len(num_list)):
            if num_list[k] == random_num:
                robot.stop()
                mqtt_client.send_message("Trigger", str(True))
                num_list = []


def review_touchdown(mqtt_client, robot, color_to_seek):
    while robot.color_sensor.color != color_to_seek:
        robot.loop_forever()
    mqtt_client.send_message("touchdown", mqtt_client, robot)


# ---------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ---------------------------------------------------------------------
main()
