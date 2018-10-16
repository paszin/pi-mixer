
from sys import argv
from threading import Thread
from time import sleep

from nuimo import Controller, ControllerManager, ControllerListener, LedMatrix


class NuimoListener(ControllerListener):
    def __init__(self, controller):
        self.controller = controller

        self.stopping = False
        self.thread = Thread(target=self.show_dots)

    def connect_succeeded(self):
        self.thread.start()

    def show_dots(self):
        num_dots = 1

        while not self.stopping:
            sleep(0.5)

            s = "{:<81}".format("*" * num_dots)
            self.controller.display_matrix(LedMatrix(s), interval=3.0, brightness=1.0, fading=True)

            num_dots += 1
            if num_dots > 81:
                num_dots = 1

    def stop(self):
        self.controller.disconnect()
        self.stopping = True


def main(mac_address):
    manager = ControllerManager(adapter_name="hci0")
    controller = Controller(mac_address=mac_address, manager=manager)
    listener = NuimoListener(controller)
    controller.listener = listener
    controller.connect()

    try:
        manager.run()
    except KeyboardInterrupt:
        print("Stopping...")
        listener.stop()
        manager.stop()


if __name__ == "__main__":

    main("E6:EF:1D:B1:E0:08")
