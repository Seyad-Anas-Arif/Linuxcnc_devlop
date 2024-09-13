import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QTextEdit, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class ButtonApp(QWidget):
    def __init__(self):
        super().__init__()
        
        # Main window properties
        self.setWindowTitle('Button Status & LED Indicator')
        self.setGeometry(100, 100, 400, 300)

        # Status window
        self.status_window = QTextEdit(self)
        self.status_window.setReadOnly(True)

        # LED label (initial color red)
        self.led_label = QLabel(self)
        self.led_label.setText('LED')
        self.led_label.setStyleSheet('background-color: red; color: white; font-size: 16px; padding: 10px;')
        self.led_label.setAlignment(Qt.AlignCenter)

        # Button names
        self.button_names = ['Start', 'Stop', 'Reset', 'Open', 'Close', 'Emergency']
        self.buttons = []

        # Create buttons
        self.create_buttons()

        # Layout for buttons
        button_layout1 = QHBoxLayout()
        button_layout2 = QHBoxLayout()

        # Add first 3 buttons to the first row
        for i in range(3):
            button_layout1.addWidget(self.buttons[i])

        # Add the next 3 buttons to the second row
        for i in range(3, 6):
            button_layout2.addWidget(self.buttons[i])

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addLayout(button_layout1)
        main_layout.addLayout(button_layout2)
        main_layout.addWidget(self.status_window)
        main_layout.addWidget(self.led_label)
        
        self.setLayout(main_layout)

    def create_buttons(self):
        """Function to create buttons"""
        for name in self.button_names:
            button = self.create_button(name)
            self.buttons.append(button)

    def create_button(self, name):
        """Create an individual button"""
        button = QPushButton(name, self)
        button.setCheckable(True)
        button.setStyleSheet('background-color: lightgray;')
        button.pressed.connect(lambda b=button: self.on_press(b))
        button.released.connect(lambda b=button: self.on_release(b))
        return button

    def on_press(self, button):
        """Handle button press event and send EtherCAT command"""
        button.setStyleSheet('background-color: green;')  # Change color when pressed
        self.status_window.append(f'{button.text()} pressed')

        # Send EtherCAT command based on the button pressed
        self.send_ethercat_command(button.text())

    def on_release(self, button):
        """Handle button release event"""
        button.setStyleSheet('background-color: lightgray;')  # Change color back after release
        self.status_window.append(f'{button.text()} released')
        self.update_led()

    def update_led(self):
        """Update the LED indicator based on button states"""
        if any(button.isChecked() for button in self.buttons):
            self.led_label.setStyleSheet('background-color: green; color: white; font-size: 16px; padding: 10px;')
        else:
            self.led_label.setStyleSheet('background-color: red; color: white; font-size: 16px; padding: 10px;')

    def send_ethercat_command(self, button_name):
        """Send command to EtherCAT based on the button pressed"""
        # This is where you'd interact with your EtherCAT setup
        # For example, send different commands based on the button
        if button_name == 'Start':
            print("Sending 'Start' command to EtherCAT")
            # Add code to send the actual EtherCAT start command
        elif button_name == 'Stop':
            print("Sending 'Stop' command to EtherCAT")
            # Add code to send the actual EtherCAT stop command
        elif button_name == 'Reset':
            print("Sending 'Reset' command to EtherCAT")
            # Add code to send the actual EtherCAT reset command
        elif button_name == 'Open':
            print("Sending 'Open' command to EtherCAT")
            # Add code to send the actual EtherCAT open command
        elif button_name == 'Close':
            print("Sending 'Close' command to EtherCAT")
            # Add code to send the actual EtherCAT close command
        elif button_name == 'Emergency':
            print("Sending 'Emergency' command to EtherCAT")
            # Add code to send the actual EtherCAT emergency command

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ButtonApp()
    window.show()
    sys.exit(app.exec_())
