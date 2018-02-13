import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com
import robot_controller as robo

COLOR_NAMES = ["None", "Black", "Blue", "Green", "Yellow", "Red", "White", "Brown"]

class DataContainer(object):
    """ Helper class that might be useful to communicate between different callbacks."""

    def __init__(self, label_to_display_messages_in):
        self.running = True
        self.display_label = label_to_display_messages_in

    def button_pressed(self, button_name):
        print("Received: " + button_name)
        message_to_display = "{} was pressed.".format(button_name)
        self.display_label.configure(text=message_to_display)

def main():

    pc_delegate = DataContainer(button_message)
    mqtt_client = com.MqttClient(pc_delegate)
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("Let's Run Errands")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    go_to_the_store_button = ttk.Button(main_frame, text="Go to the Store")
    go_to_the_store_button.grid(row=0, column=0)
    go_to_the_store_button['command'] = lambda: color_seek(
        mqtt_client, 'blue')

    go_to_school_button = ttk.Button(main_frame, text="Go to school")
    go_to_school_button.grid(row=0, column=2)
    go_to_school_button['command'] = lambda: color_seek(
        mqtt_client, 'green')

    go_home_button = ttk.Button(main_frame, text="Go home")
    go_home_button.grid(row=2, column=0)
    go_home_button['command'] = lambda: color_seek(
    mqtt_client, 'red')

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=2, column=2)
    q_button['command'] = lambda: quit_program(mqtt_client, False)

    root.mainloop()

def send_color_demand(mqtt_client, color_to_seek):
    print('Seeking LED color = {}'.format(color_to_seek))
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