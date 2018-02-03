"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time

MAX_SPEED = 900

class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    def __init__(self):
        # Connect two large motors on output ports B and C
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.max_speed = 900
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()

        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor

    def drive_inches(self, inch_target, speed):
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = inch_target * \
                                        degrees_per_inch
        self.left_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees,
            speed_sp=speed,
            stop_action="brake")
        self.right_motor.run_to_rel_pos(
            position_sp=motor_turns_needed_in_degrees, speed_sp=speed,
            stop_action="brake")
        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):
        length = math.fabs(degrees_to_turn) * 0.049
        degrees_per_inch = 90
        motor_turns_needed_in_degrees = length * \
                                        degrees_per_inch
        if degrees_to_turn > 0:
            self.left_motor.run_to_rel_pos(
                position_sp=-motor_turns_needed_in_degrees,
                speed_sp=turn_speed_sp,
                stop_action="brake")
            self.right_motor.run_to_rel_pos(
                position_sp=motor_turns_needed_in_degrees, speed_sp=turn_speed_sp,
                stop_action="brake")
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

        elif degrees_to_turn < 0:
            self.left_motor.run_to_rel_pos(
                position_sp=motor_turns_needed_in_degrees,
                speed_sp=turn_speed_sp,
                stop_action="brake")
            self.right_motor.run_to_rel_pos(
                position_sp=-motor_turns_needed_in_degrees,
                speed_sp=turn_speed_sp,
                stop_action="brake")
            self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
            self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def arm_calibration(self):
        self.arm_motor.run_forever(speed_sp=self.max_speed)

        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)

        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep()

        self.arm_motor.position = 0

    def arm_up(self):
        self.arm_motor.run_forever(speed_sp=self.max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.max_speed)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

    def shutdown(self):
        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

        print('Goodbye')
        ev3.Sound.speak("Goodbye").wait()