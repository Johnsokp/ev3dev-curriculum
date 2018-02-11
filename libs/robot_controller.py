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
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")


        # Check that the motors are actually connected
        assert self.left_motor.connected
        assert self.right_motor.connected
        assert self.arm_motor.connected
        assert self.touch_sensor
        assert self.color_sensor
        assert self.ir_sensor
        assert self.pixy

    def drive_inches(self, inch_target, speed):
        """drives robot forward or backward at a specified speed depending on
        whether the distance is postive or negative"""

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
        """Turns robot to the specified degree at a specified speed. Turns
        left if the degree is positive and right if the degree is negative."""

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
        """Lifts the robots arm until the touch sensor is pressed, then it
        lowers the arm 14.2 revolutions and sets the position to 0"""

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
        """Lifts the robots arm until the touch sensor is pressed, then it
        stops"""

        self.arm_motor.run_forever(speed_sp=self.max_speed)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action="brake")
        ev3.Sound.beep()

    def arm_down(self):
        """Lowers the arms to the 0 position defined from calibration"""

        self.arm_motor.run_to_abs_pos(position_sp=0, speed_sp=self.max_speed)
        self.arm_motor.wait_while(
            ev3.Motor.STATE_RUNNING)  # Blocks until the motor finishes running
        ev3.Sound.beep()

    def shutdown(self):
        """Stops all robot actions and exits code"""

        self.running = False

        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")

        ev3.Leds.set_color(ev3.Leds.LEFT, ev3.Leds.GREEN)
        ev3.Leds.set_color(ev3.Leds.RIGHT, ev3.Leds.GREEN)

        print('Goodbye')
        ev3.Sound.speak("Goodbye").wait()

    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(
                0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def stop(self):
        """Stops all robot actions"""

        self.left_motor.stop(stop_action="brake")
        self.right_motor.stop(stop_action="brake")
        self.arm_motor.stop(stop_action="brake")

    def forward(self, left_speed_entry, right_speed_entry):
        """moves robot forward at specified speed"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def left(self, left_speed_entry):
        """moves robots left track forward at specified speed"""
        self.left_motor.run_forever(speed_sp=left_speed_entry)

    def back(self, left_speed_entry, right_speed_entry):
        """moves robot back at specified speed"""
        self.left_motor.run_forever(speed_sp=-left_speed_entry)
        self.right_motor.run_forever(speed_sp=-right_speed_entry)

    def right(self, right_speed_entry):
        """moves robots right track forward at specified speed"""
        self.right_motor.run_forever(speed_sp=right_speed_entry)

    def seek_beacon(self):
        """
        Uses the IR Sensor in BeaconSeeker mode to find the beacon.  If the beacon is found this return True.
        If the beacon is not found and the attempt is cancelled by hitting the touch sensor, return False.
        """
        forward_speed = 300
        turn_speed = 100

        # To find the IR beacon (with the remote in beacon mode)
        beacon_seeker = ev3.BeaconSeeker()  # Assumes remote is set to channel 1
        print("Heading", beacon_seeker.heading)
        print("Distance", beacon_seeker.distance)

        while not self.touch_sensor.is_pressed:
            current_heading = beacon_seeker.heading  # use the beacon_seeker
            # heading
            current_distance = beacon_seeker.distance  # use the beacon_seeker distance

            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                print("IR Remote not found. Distance is -128")
                self.stop()
            else:
                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    if current_distance <= 1:
                        self.stop()
                        print(forward_speed)
                        self.drive_inches(3, forward_speed)
                        print('great')

                        return True
                    else:
                        self.forward(forward_speed, forward_speed)
                elif math.fabs(current_heading) < 10:
                    if current_heading < 0:
                        self.forward(-turn_speed, turn_speed)
                    elif current_heading > 0:
                        self.forward(turn_speed, -turn_speed)
                else:
                    print("Heading is too far off to fix: ", current_heading)

            time.sleep(0.02)

        # The touch_sensor was pressed to abort the attempt if this code runs.
        print("Abandon ship!")
        robot.stop()
        return False
