import robot_controller as robo
import mqtt_remote_method_calls as com

import ev3dev.ev3 as ev3
import time

class DataContainer(object):

    def __init__(self):
        self.running = True

    def drive_to_color(self, color_to_seek):
        print("Received: {} {}".format(color_to_seek))

        while robot.color_sensor.color != color_to_seek:
            robot.forward(100, 100)
            print(robot.color_sensor.color)
        robot.stop()

def main():
    robot = robo.Snatch3r()
    dc = DataContainer()

    ev3_delegate = DataContainer()
    mqtt_client = com.MqttClient(ev3_delegate)
    mqtt_client.connect_to_pc()

    print("--------------------------------------------")
    print("Let's run errands")
    print("--------------------------------------------")
    ev3.Sound.speak("Let's run errands").wait()

    while dc.running:
        btn.process()
        time.sleep(0.01)

    btn = ev3.Button()
    btn.on_up = lambda state: handle_button_press(state, mqtt_client, "Up")
    btn.on_down = lambda state: handle_button_press(state, mqtt_client, "Down")
    btn.on_left = lambda state: handle_button_press(state, mqtt_client, "Left")
    btn.on_right = lambda state: handle_button_press(state, mqtt_client,
                                                     "Right")
    btn.on_backspace = lambda state: handle_shutdown(state, ev3_delegate)

def handle_button_press(button_state, mqtt_client, button_name):
    if button_state:
        print("{} button was pressed".format(button_name))
        mqtt_client.send_message("button_pressed",
                                 [button_name])

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


main()
