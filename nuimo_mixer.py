import nuimo

NUIMO_ADDRESS = "E6:EF:1D:B1:E0:08"



class ControllerPrintListener(nuimo.ControllerListener):
    """
    An implementation of ``ControllerListener`` that prints each event.
    """
    def __init__(self, controller):
        self.controller = controller
        self.mode = "default"

    def started_connecting(self):

        print("connecting...")

    def connect_succeeded(self):
        print("connected")

    def connect_failed(self, error):
        print("connect failed: " + str(error))

    def started_disconnecting(self):
        print("disconnecting...")

    def disconnect_succeeded(self):
        print("disconnected")

    def received_gesture_event(self, event):
        matrix = nuimo.LedMatrix(
        "*       *"
        " *     * "
        "  *   *  "
        "   * *   "
        "    *    "
        "   * *   "
        "  *   *  "
        " *     * "
        "*       *"
        )
        self.controller.display_matrix(matrix, interval=10)
        print(event.gesture,event.gesture == nuimo.Gesture.ROTATION)
        if (event.gesture == nuimo.Gesture.ROTATION):
            print(event.value)
        if (event.gesture == nuimo.Gesture.BUTTON_PRESS):
            pass



if __name__ == '__main__':
    manager = nuimo.ControllerManager(adapter_name='hci0')

    controller = nuimo.Controller(mac_address=NUIMO_ADDRESS, manager=manager)
    controller.listener = ControllerPrintListener(controller) # Use an instance of your own nuimo.ControllerListener subclass
    controller.connect()
    matrix = nuimo.LedMatrix(
    "*       *"
    " *     * "
    "  *   *  "
    "   * *   "
    "    *    "
    "   * *   "
    "  *   *  "
    " *     * "
    "*       *"
    )
    controller.display_matrix(matrix)

    manager.run()
