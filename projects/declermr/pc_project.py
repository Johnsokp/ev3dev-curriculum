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

import mqtt_remote_method_calls as com

import tkinter
from tkinter import ttk

import random


class WindowDelegate(object):
    def __init__(self):
        self.old_window = tkinter.Tk()
        self.new_window = tkinter.Toplevel()
        self.left_speed_number = 500
        self.right_speed_number = 500
        self.trigger = False
        self.running = True

    def next_window(self):
        if self.trigger:
            self.old_window.destroy()


def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    window = WindowDelegate()

    root = tkinter.Tk()

    master_gui(mqtt_client, root, window)

    root.mainloop()


# ----------------------------------------------------------------------
# Tkinter callbacks
# ----------------------------------------------------------------------


def drive_forward(mqtt_client, left_speed_number, right_speed_number):
    mqtt_client.send_message("forward", [left_speed_number, right_speed_number])


def turn_right(mqtt_client, right_speed_number, left_speed_number):
    mqtt_client.send_message("left", [left_speed_number])
    mqtt_client.send_message("right", [-right_speed_number])


def stop(mqtt_client):
    mqtt_client.send_message("stop")


def turn_left(mqtt_client, right_speed_number, left_speed_number):
    mqtt_client.send_message("right", [right_speed_number])
    mqtt_client.send_message("left", [-left_speed_number])


def drive_back(mqtt_client, left_speed_number, right_speed_number):
    mqtt_client.send_message("back", [left_speed_number, right_speed_number])


# Quit and Exit button callbacks
def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


# ----------------------------------------------------------------------
# Windows
# ----------------------------------------------------------------------

def master_gui(mqtt_client, root, window):
    if not window.trigger:
        window1(mqtt_client, root, window)
    else:
        window2(root, window)


def window1(mqtt_client, root, window):
    root.title("Score a touchdown")

    running_frame = ttk.Frame(root, padding=20, relief='raised')
    running_frame.grid()

    # picture = tkinter.PhotoImage(file='runningback_image.gif')
    # not_a_button = ttk.Button(running_frame, image=picture)
    # not_a_button.image = picture
    # not_a_button.grid(row=1, column=0)
    # not_a_button['command'] = lambda: print('Eyes on the ball rookie!')

    forward_button = ttk.Button(running_frame, text="Forward")
    forward_button.grid(row=2, column=2)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: drive_forward(mqtt_client, window.left_speed_number, window.right_speed_number)
    root.bind('<Up>', lambda event: drive_forward(mqtt_client, window.left_speed_number, window.right_speed_number))

    left_button = ttk.Button(running_frame, text="Turn Left")
    left_button.grid(row=3, column=1)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, window.right_speed_number, window.left_speed_number)
    root.bind('<Left>', lambda event: turn_left(mqtt_client, window.right_speed_number, window.left_speed_number))

    right_button = ttk.Button(running_frame, text="Turn Right")
    right_button.grid(row=3, column=3)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, window.right_speed_number, window.left_speed_number)
    root.bind('<Right>', lambda event: turn_right(mqtt_client, window.right_speed_number, window.left_speed_number))

    back_button = ttk.Button(running_frame, text="Back")
    back_button.grid(row=4, column=2)
    # back_button and '<Down>' key
    back_button['command'] = lambda: drive_back(mqtt_client, window.left_speed_number, window.right_speed_number)
    root.bind('<Down>', lambda event: drive_back(mqtt_client, window.left_speed_number, window.right_speed_number))

    stop_button = ttk.Button(running_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    root.bind('<space>', lambda event: stop(mqtt_client))

    q_button = ttk.Button(running_frame, text="Fumble, Lose Possession")
    q_button.grid(row=5, column=0)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(running_frame, text="Out with an Injury")
    e_button.grid(row=5, column=4)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))


def window2(root, window):
    window.next_window()
    root_2 = tkinter.Toplevel()
    root.title("TACKLE INCOMING!!!")

    dodge_frame = ttk.Frame(root_2, padding=20, relief='raised')
    dodge_frame.grid()

    pic = tkinter.PhotoImage(file='tackle_image.gif')
    also_not_a_button = ttk.Button(dodge_frame, image=pic)
    also_not_a_button.image = pic
    also_not_a_button.grid(row=0, column=0)
    also_not_a_button['command'] = lambda: print('Stop standing there and shake him off!')

    dodge_label = ttk.Label(dodge_frame, text="Dodge Left or Right")
    dodge_label.grid(row=1, column=0)
    dodge_entry = ttk.Entry(dodge_frame, width=8)
    dodge_entry.insert(0, "")
    dodge_entry.grid(row=2, column=0)
    dodge_entry['command'] = lambda: dodge(dodge_entry, window)


# ----------------------------------------------------------------------
# Custom callbacks
# ----------------------------------------------------------------------

def touchdown(mqtt_client, robot):
    robot.running = False
    mqtt_client.send_message("drive_inches", int(3), int(600))


def dodge(dodge_entry, window):
    random_num = random.randrange(1, 2)
    if random_num == 1:
        dodge_direction = "left"
    else:
        dodge_direction = "right"

    if dodge_direction == dodge_entry:
        window.trigger = True
    else:
        window.running = False


# def play_wav_file():
    # File from
    # Had to convert it to a PCM signed 16-bit little-endian .wav file
    # http://audio.online-convert.com/convert-to-wav
    # ev3.Sound.play("/home/robot/csse120/projects/declermr/_____________.wav")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------

main()
