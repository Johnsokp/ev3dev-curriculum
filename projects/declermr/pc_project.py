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

Author: Matthew De Clerck
Supporting Code Authors: Matthew De Clerck, Caitlin Coverstone, Kynon Johnson
"""

import mqtt_remote_method_calls as com

import tkinter
from tkinter import ttk

import random


class WindowDelegate(object):
    def __init__(self):
        self.left_speed_number = 100
        self.right_speed_number = 100
        self.trigger = False
        self.running = True
        self.flip = 0
        self.root = tkinter.Tk()

    def triggered(self, trigger_switch):
        self.flip = 1
        self.trigger = trigger_switch

    def touchdown(self):
        self.root.destroy()


def main():
    window = WindowDelegate()

    mqtt_client = com.MqttClient(window)
    mqtt_client.connect_to_ev3()

    main_root = window.root
    secondary_root = tkinter.Toplevel()
    tertiary_root = tkinter.Toplevel()
    main_root.after(500, lambda: master_gui(main_root, secondary_root, tertiary_root, window))
    window1(mqtt_client, secondary_root, window)
    window2(tertiary_root, window)
    main_root.withdraw()
    tertiary_root.iconify()

    main_root.mainloop()

# ----------------------------------------------------------------------
# Windows
# ----------------------------------------------------------------------


def master_gui(root, secondary_root, tertiary_root, window):
    if window.flip == 1:
        if not window.trigger:
            tertiary_root.iconify()
            secondary_root.deiconify()
            window.flip = 0
        else:
            secondary_root.iconify()
            tertiary_root.deiconify()
            window.flip = 0
    root.after(500, lambda: master_gui(root, secondary_root, tertiary_root, window))


def window1(mqtt_client, secondary_root, window):
    secondary_root.title("Score a touchdown")

    running_frame = ttk.Frame(secondary_root, padding=20, relief='raised')
    running_frame.grid()

    picture = tkinter.PhotoImage(file='runningback_image.gif')
    not_a_button = ttk.Button(running_frame, image=picture)
    not_a_button.image = picture
    not_a_button.grid(row=1, column=2)
    not_a_button['command'] = lambda: print('Eyes on the ball rookie!')

    forward_button = ttk.Button(running_frame, text="Forward")
    forward_button.grid(row=2, column=2)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: drive_forward(mqtt_client, window.left_speed_number, window.right_speed_number)
    secondary_root.bind('<Up>',
                        lambda event: drive_forward(mqtt_client, window.left_speed_number, window.right_speed_number))

    left_button = ttk.Button(running_frame, text="Turn Left")
    left_button.grid(row=3, column=1)
    # left_button and '<Left>' key
    left_button['command'] = lambda: turn_left(mqtt_client, window.right_speed_number, window.left_speed_number)
    secondary_root.bind('<Left>',
                        lambda event: turn_left(mqtt_client, window.right_speed_number, window.left_speed_number))

    right_button = ttk.Button(running_frame, text="Turn Right")
    right_button.grid(row=3, column=3)
    # right_button and '<Right>' key
    right_button['command'] = lambda: turn_right(mqtt_client, window.right_speed_number, window.left_speed_number)
    secondary_root.bind('<Right>',
                        lambda event: turn_right(mqtt_client, window.right_speed_number, window.left_speed_number))

    back_button = ttk.Button(running_frame, text="Back")
    back_button.grid(row=4, column=2)
    # back_button and '<Down>' key
    back_button['command'] = lambda: drive_back(mqtt_client, window.left_speed_number, window.right_speed_number)
    secondary_root.bind('<Down>',
                        lambda event: drive_back(mqtt_client, window.left_speed_number, window.right_speed_number))

    stop_button = ttk.Button(running_frame, text="Stop")
    stop_button.grid(row=3, column=2)
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
    stop_button['command'] = lambda: stop(mqtt_client)
    secondary_root.bind('<space>', lambda event: stop(mqtt_client))

    q_button = ttk.Button(running_frame, text="Fumble, Lose Possession")
    q_button.grid(row=5, column=0)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    e_button = ttk.Button(running_frame, text="Out with an Injury")
    e_button.grid(row=5, column=4)
    e_button['command'] = (lambda: quit_program(mqtt_client, True))


def window2(root, window):
    root.title("TACKLE INCOMING!!!")

    dodge_frame = ttk.Frame(root, padding=20, relief='raised')
    dodge_frame.grid()

    pic = tkinter.PhotoImage(file='tackle_image.gif')
    also_not_a_button = ttk.Button(dodge_frame, image=pic)
    also_not_a_button.image = pic
    also_not_a_button.grid(row=0, column=0)
    also_not_a_button['command'] = lambda: print('Stop standing there and shake him off!')

    dodge_label = ttk.Label(dodge_frame, text="Dodge Left or Right")
    dodge_label.grid(row=1, column=0)

    dodge_entry = ttk.Entry(dodge_frame, width=8)
    dodge_entry.grid(row=2, column=0)

    dodge_button = ttk.Button(dodge_frame, text="Dodge")
    dodge_button.grid(row=3, column=0)
    dodge_button['command'] = lambda: dodge(dodge_entry.get(), window)
    root.bind('<Return>', lambda event:  dodge(dodge_entry.get(), window))


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
# Custom callbacks
# ----------------------------------------------------------------------


def dodge(dodge_entry, window):
    random_num = random.randrange(1, 2)
    if random_num == 1:
        dodge_direction = "left"
        other_dodge_direction = "Left"
    else:
        dodge_direction = "right"
        other_dodge_direction = "Right"

    if dodge_direction == dodge_entry or other_dodge_direction == dodge_entry:
        window.triggered(False)
        print(5)
    else:
        window.running = False
        print(6)


# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------

main()
