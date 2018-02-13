import robot_controller as robo


COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True

def main():
    robot = robo.Snatch3r()
    dc = DataContainer()

    print("--------------------------------------------")
    print("Let's run errands")
    print("--------------------------------------------")
    ev3.Sound.speak("Let's run errands").wait()

    white_level = 50
    black_level = 40

    while dc.running:
        btn.process()
        time.sleep(0.01)

    #while True:
    #    command_to_run = input("Enter w (white), b (black), store, school,
        # home or quit: ")
    #    if command_to_run == 'w':
    #        print("Calibrate the white light level")

    #        print(robot.color_sensor.reflected_light_intensity)

    #        white_level = robot.color_sensor.reflected_light_intensity

    #        print("New white level is {}.".format(white_level))
    #    elif command_to_run == 'b':
    #        print("Calibrate the black light level")

     #       print(robot.color_sensor.reflected_light_intensity)

    #        black_level = robot.color_sensor.reflected_light_intensity

     #       print("New black level is {}.".format(black_level))

     #   elif command_to_run == 'store':
     #       print("Going to the store")
     #       ev3.Sound.speak("Going to the store").wait()
     #       follow_the_line(robot, white_level, black_level)
     #   elif command_to_run == 'school':
     #       print("Going to school")
      #      ev3.Sound.speak("Going to school").wait()
    #    elif command_to_run == 'home':
     #       print("Going home")
       #     ev3.Sound.speak("Going to school").wait()
     #       follow_the_line(robot, white_level, black_level)
     #   elif command_to_run == 'quit':
     #       break
    #    else:
    #        print(command_to_run, "is not a known command. Please enter a
    # valid choice.")

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()

def drive_to_color(button_state, robot, color_to_seek):
    """
    When the button_state is True (pressed), drives the robot forward until the desired color is detected.
    When the color_to_seek is detected the robot stops moving forward and speaks a message.

    Type hints:
      :type button_state: bool
      :type robot: robo.Snatch3r
      :type color_to_seek: int
    """
    if button_state:
        ev3.Sound.speak("Seeking " + COLOR_NAMES[color_to_seek]).wait()

        while robot.color_sensor.color != color_to_seek:
            robot.forward(100, 100)
            print(robot.color_sensor.color)

        robot.stop()
    ev3.Sound.speak("Found " + COLOR_NAMES[color_to_seek]).wait()

def follow_the_line(robot, white_level, black_level):
    """
    The robot follows the black line until the touch sensor is pressed.
    You will need a black line track to test your code
    When the touch sensor is pressed, line following ends, the robot stops, and control is returned to main.

    Type hints:
      :type robot: robo.Snatch3r
      :type white_level: int
      :type black_level: int
    """

    x = 1
    while x == 1:
        if robot.color_sensor.reflected_light_intensity >= black_level + 20:
            robot.turn_degrees(-10, 200)
        else:
            robot.forward(600, 600)
        if robot.touch_sensor.is_pressed:
            break

    robot.stop()
    ev3.Sound.speak("Done")

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()




# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()
