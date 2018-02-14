"""
The purpose of this program is to run on the computer portion using MQTT to communicate with the EV3 robot
and interacts back and forth.

The premise is a simulation of football running back where at any point the 'player' is about to be tackled.
The player rides around on a piece of paper simulating a 'muddy field,' and the mud is more frequent towards
the center of the field. The code runs a random number generator, and every number is a chance of being
tackled by another player. Once the chance appears a window opens where you have 3 seconds to decide whether
to go left or right to dodge. The correct answer is also random.

Failure resets all accumulated variables to empty, and sends the player back to the middle.
Success is where the player is able to get a touchdown. The robot will celebrate by moving the arm up and down
while spinning in a circle.

The robot will be controlled by using the buttons on a GUI or the keyboard. This is overridden when the player
is in a tackle event, and the player will be tackled soon.

Stretch goal: feedback on a screen of where the player is.

Author: Matthew De Clerck
Supporting Code Authors: Matthew De Clerck, Caitlin Coverstone, Kynon Johnson
"""

import robot_controller as robo

import mqtt_remote_method_calls as com

import tkinter
from tkinter import ttk


def main():
    robot = robo.Snatch3r()

    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()

    left_speed_number = 500
    right_speed_number = 500

    num_list = []
    trigger = False
    mqtt_client.send_message("mud", [mqtt_client, robot, robo.ev3.ColorSensor.COLOR_BROWN, num_list])

    while robot.running:
        if not trigger:
            root.title("Score a touchdown")
            main_frame = ttk.Frame(root, padding=20, relief='raised')
            main_frame.grid()

            picture = tkinter.PhotoImage(file="running-back-image.jpg")
            not_a_button = ttk.Button(main_frame, image=picture)
            not_a_button.image = picture
            not_a_button.grid(row=1, column=0)
            not_a_button['command'] = lambda: print('Eyes on the ball rookie!')

            forward_button = ttk.Button(main_frame, text="Forward")
            forward_button.grid(row=2, column=0)
            # forward_button and '<Up>' key is done for your here...
            forward_button['command'] = lambda: drive_forward(mqtt_client, left_speed_number, right_speed_number)
            root.bind('<Up>', lambda event: drive_forward(mqtt_client, left_speed_number, right_speed_number))

            left_button = ttk.Button(main_frame, text="Turn Left")
            left_button.grid(row=3, column=0)
            # left_button and '<Left>' key
            left_button['command'] = lambda: turn_left(mqtt_client, left_speed_number)
            root.bind('<Left>', lambda event: turn_left(mqtt_client, left_speed_number))

            right_button = ttk.Button(main_frame, text="Turn Right")
            right_button.grid(row=3, column=2)
            # right_button and '<Right>' key
            right_button['command'] = lambda: turn_right(mqtt_client, right_speed_number)
            root.bind('<Right>', lambda event: turn_right(mqtt_client, right_speed_number))

            back_button = ttk.Button(main_frame, text="Back")
            back_button.grid(row=4, column=1)
            # back_button and '<Down>' key
            back_button['command'] = lambda: drive_back(mqtt_client, left_speed_number, right_speed_number)
            root.bind('<Down>', lambda event: drive_back(mqtt_client, left_speed_number, right_speed_number))

            stop_button = ttk.Button(main_frame, text="Stop")
            stop_button.grid(row=3, column=1)
            # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
            stop_button['command'] = lambda: robot.stop()
            root.bind('<space>', lambda event: robot.stop())

            up_button = ttk.Button(main_frame, text="Up")
            up_button.grid(row=5, column=0)
            up_button['command'] = lambda: robot.arm_up()
            root.bind('<u>', lambda event: robot.arm_up())

            down_button = ttk.Button(main_frame, text="Down")
            down_button.grid(row=6, column=0)
            down_button['command'] = lambda: robot.arm_down()
            root.bind('<j>', lambda event: robot.arm_down())

            # Buttons for quit and exit
            q_button = ttk.Button(main_frame, text="Quit")
            q_button.grid(row=5, column=2)
            q_button['command'] = (lambda: robot.stop())

            e_button = ttk.Button(main_frame, text="Exit")
            e_button.grid(row=6, column=2)
            e_button['command'] = (lambda: robot.shutdown())

            root.mainloop()
        else:
            root.title("TACKLE INCOMING!!!")
            main_frame = ttk.Frame(root, padding=20, relief='raised')
            main_frame.grid()

            dodge_label = ttk.Label(main_frame, text="Dodge Left or Right")
            dodge_label.grid(row=0, column=0)
            dodge_entry = ttk.Entry(main_frame, width=8)
            dodge_entry.insert(0, "")
            dodge_entry.grid(row=1, column=0)

# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def drive_forward(mqtt_client, left_speed_number, right_speed_number):

    print("forward")
    mqtt_client.send_message("forward", [left_speed_number, right_speed_number])


def turn_right(mqtt_client, left_speed_number):
    print("left")
    mqtt_client.send_message("left", [left_speed_number])


def stop(mqtt_client):
    print("stop")
    mqtt_client.send_message("stop")


def turn_left(mqtt_client, right_speed_number):
    print("right")
    mqtt_client.send_message("right", [right_speed_number])


def drive_back(mqtt_client, left_speed_number, right_speed_number):
    print("back")
    mqtt_client.send_message("back", [left_speed_number, right_speed_number])


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Custom callbacks
# ----------------------------------------------------------------------

def touchdown(mqtt_client, robot):
    robot.running = False
    mqtt_client.send_message("drive_inches", int(3), int(600))


# def play_wav_file():
    # File from
    # Had to convert it to a PCM signed 16-bit little-endian .wav file
    # http://audio.online-convert.com/convert-to-wav
    # ev3.Sound.play("/home/robot/csse120/projects/declermr/_____________.wav")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------

main()
