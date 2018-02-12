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

    btn = robot.Button()

    left_speed_entry = 500
    right_speed_entry = 500

    trigger = False

    while robot.running:
        btn.process()
        if trigger == False:
            root.title("Score a touchdown")
            main_frame = ttk.Frame(root, padding=20, relief='raised')
            main_frame.grid()



            forward_button = ttk.Button(main_frame, text="Forward")
            forward_button.grid(row=2, column=1)
            # forward_button and '<Up>' key is done for your here...
            forward_button['command'] = lambda: robot.forward(left_speed_entry, right_speed_entry)
            root.bind('<Up>', lambda event: robot.forward(left_speed_entry, right_speed_entry))

            left_button = ttk.Button(main_frame, text="Left")
            left_button.grid(row=3, column=0)
            # left_button and '<Left>' key
            left_button['command'] = lambda: robot.left(left_speed_entry)
            root.bind('<Left>', lambda event: robot.left(left_speed_entry))

            stop_button = ttk.Button(main_frame, text="Stop")
            stop_button.grid(row=3, column=1)
            # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)
            stop_button['command'] = lambda: robot.stop()
            root.bind('<space>', lambda event: robot.stop())

            right_button = ttk.Button(main_frame, text="Right")
            right_button.grid(row=3, column=2)
            # right_button and '<Right>' key
            right_button['command'] = lambda: robot.right(left_speed_entry)
            root.bind('<Right>', lambda event: robot.right(left_speed_entry))

            back_button = ttk.Button(main_frame, text="Back")
            back_button.grid(row=4, column=1)
            # back_button and '<Down>' key
            back_button['command'] = lambda: robot.back(left_speed_entry,
                                                        right_speed_entry)
            root.bind('<Down>', lambda event: robot.back(left_speed_entry,
                                                    right_speed_entry))

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
            q_button['command'] = (lambda: robot.quit_program(False))

            e_button = ttk.Button(main_frame, text="Exit")
            e_button.grid(row=6, column=2)
            e_button['command'] = (lambda: robot.quit_program(True))

            root.mainloop()
        else:
            root.title("TACKLE INCOMING!!!")
            main_frame = ttk.Frame(root, padding=20, relief='raised')
            main_frame.grid()

            left_speed_label = ttk.Label(main_frame, text="Left")
            left_speed_label.grid(row=0, column=0)
            left_speed_entry = ttk.Entry(main_frame, width=8)
            left_speed_entry.insert(0, "600")
            left_speed_entry.grid(row=1, column=0)

            right_speed_label = ttk.Label(main_frame, text="Right")
            right_speed_label.grid(row=0, column=2)
            right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
            right_speed_entry.insert(0, "600")
            right_speed_entry.grid(row=1, column=2)

def play_wav_file():
    # File from
    # Had to convert it to a PCM signed 16-bit little-endian .wav file
    # http://audio.online-convert.com/convert-to-wav
    #ev3.Sound.play("/home/robot/csse120/projects/declermr/_____________.wav")

# ----------------------------------------------------------------------
# Calls  main  to start the ball rolling.
# ----------------------------------------------------------------------
main()


