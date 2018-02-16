"""
This section serves as the base code running on the EV3. Its job is to make sure the EV3 is able to move according
to the input that is received. It also sends feedback regarding the status of the EV3 and its environment.

The EV3 is programmed to receive a signal from the computer to move around. This is done using the MQTT that it
and the computer uses as a communication device. The program ends
"""

import mqtt_remote_method_calls as com

import robot_controller as robo

import random


# Potential values of the color_sensor.color property
#   ev3.ColorSensor.COLOR_NOCOLOR is the value 0
#   ev3.ColorSensor.COLOR_BLACK   is the value 1
#   ev3.ColorSensor.COLOR_BLUE    is the value 2
#   ev3.ColorSensor.COLOR_GREEN   is the value 3
#   ev3.ColorSensor.COLOR_YELLOW  is the value 4
#   ev3.ColorSensor.COLOR_RED     is the value 5
#   ev3.ColorSensor.COLOR_WHITE   is the value 6
#   ev3.ColorSensor.COLOR_BROWN   is the value 7
COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]


def main():
    robo.ev3.Sound.speak("test test").wait()

    robot = robo.Snatch3r()
    mqtt_client = com.MqttClient(robot)
    mqtt_client.connect_to_pc()

    robot.arm_calibration()

    btn = robo.ev3.Button()
    btn.on_backspace = lambda state: handle_shutdown(state, robot)

    num_list = []

    """
    Stretch goal: implement button functions for celebration
    """
    # btn.on_up = lambda state:
    # btn.on_down = lambda state:
    # btn.on_left = lambda state:
    # btn.on_right = lambda state:

    while robot.running:
        btn.process()
        review_touchdown(mqtt_client, robot, robo.ev3.ColorSensor.COLOR_BLUE)
        mud(mqtt_client, robot, robo.ev3.ColorSensor.COLOR_BROWN, num_list)


# ----------------------------------------------------------------------
# Sense the color.
# ----------------------------------------------------------------------


def mud(mqtt_client, robot, color_to_seek, num_list):
    random_num = random.randrange(1, 100)
    if robot.color_sensor.color == color_to_seek:
        num_list.append(random_num)
        for k in range(len(num_list)):
            if num_list[k] == random_num:
                robot.stop()
                mqtt_client.send_message("Trigger", [str(True)])
                num_list = []
        robo.time.sleep(.5)


def review_touchdown(mqtt_client, robot, color_to_seek):
    if robot.color_sensor.color == color_to_seek:
        mqtt_client.send_message("touchdown", [mqtt_client, robot])


def handle_shutdown(button_state, robot):
    """Exit the program."""
    if button_state:
        robot.shutdown()


# ---------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ---------------------------------------------------------------------
main()
