import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self):
        self.running = True

def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Let's Run Errands")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    go_to_the_store_button = ttk.Button(main_frame, text="Go to the Store")
    go_to_the_store_button.grid(row=0, column=0)
    go_to_the_store_button['command'] = lambda: color_seek(
        mqtt_client, ev3.ColorSensor.COLOR_RED)

    go_to_school_button = ttk.Button(main_frame, text="Go to school")
    go_to_school_button.grid(row=0, column=2)
    go_to_school_button['command'] = lambda: color_seek(
        mqtt_client, ev3.ColorSensor.COLOR_BLUE)

    go_home_button = ttk.Button(main_frame, text="Go home")
    go_home_button.grid(row=2, column=0)
    go_home_button['command'] = lambda: color_seek(
    mqtt_client, ev3.ColorSensor.COLOR_GREEN)

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=2, column=2)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    root.mainloop()

def color_seek(mqtt_client, color_to_seek):
    print('Seeking' + COLOR_NAMES[color_to_seek])
    mqtt_client.send_message("drive_to_color", [color_to_seek])
    

def drive_to_color(mqtt_client, color_to_seek):
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

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()