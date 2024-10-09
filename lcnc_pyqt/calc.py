import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout, QLabel, QDial
from PyQt5.QtCore import QSize, Qt  # Import Qt for alignment
from PyQt5.QtGui import QPainter, QColor, QBrush, QFont

class LEDButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.led_on = False  # Default LED state is OFF
        self.setFont(QFont('Arial', 12, QFont.Bold))
        self.setFixedSize(120, 60)  # Set fixed size for buttons

    def toggle_led(self):
        """Toggle the LED state when the button is pressed."""
        self.led_on = not self.led_on
        self.update()  # Trigger a repaint of the button

    def paintEvent(self, event):
        """Override the paintEvent to draw the button and the LED."""
        super().paintEvent(event)

        # Create QPainter object to draw the LED on the button
        painter = QPainter(self)

        # Set the LED color based on the current state
        led_color = QColor("green") if self.led_on else QColor("red")

        # Set the painter's brush to the LED color
        painter.setBrush(QBrush(led_color))

        # Draw the LED (small circle) on the top-right corner of the button
        led_size = 10
        painter.drawEllipse(self.width() - led_size - 10, 10, led_size, led_size)
        if self.led_on:
            led_color= QColor("green")
        elif self.led_off:
            led_color= QColor("red")

class LEDButtonPanel(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buttons with Integrated LED, Status Panel, and Dial")
        self.setGeometry(100, 100, 300, 400)

        # Create buttons with integrated LED
        self.start_btn = LEDButton(" START")
        self.fwd_btn = LEDButton("Forward")
        self.rev_btn = LEDButton("Reverse")

        # Status panel to display messages
        self.status_label = QLabel("Motor - Ready", self)
        self.status_label.setFont(QFont('Arial', 10))
        self.status_label.setStyleSheet("background-color: #e0e0e0; padding: 10px; border: 1px solid #333333;")
        self.status_label.setAlignment(Qt.AlignCenter)  # Align text to center

        # Create a QDial (rotary dial widget)
        self.dial = QDial(self)
        self.dial.setMinimum(0)
        self.dial.setMaximum(100)
        self.dial.setValue(50)  # Set default value for the dial
        self.dial.valueChanged.connect(self.dial_value_changed)  # Connect dial movement to status update

        # Connect the buttons to toggle their LED and update the status panel
        self.start_btn.clicked.connect(lambda: self.update_status(self.start_btn, " Start"))
        self.start_btn.clicked.connect(self.start_btn.toggle_led);
        self.fwd_btn.clicked.connect(lambda: self.update_status(self.fwd_btn, "forward"))
        self.fwd_btn.clicked.connect(self.fwd_btn.toggle_led);
        self.rev_btn.clicked.connect(lambda: self.update_status(self.rev_btn, "Reverse."))
        self.rev_btn.clicked.connect(self.rev_btn.toggle_led);

        # Layout to organize buttons, dial, and status panel vertically
        layout = QVBoxLayout()
        layout.addWidget(self.start_btn)
        layout.addWidget(self.fwd_btn)
        layout.addWidget(self.rev_btn)
        layout.addWidget(self.dial)  # Add the QDial to the layout
        layout.addWidget(self.status_label)  # Add the status label at the bottom

        self.setLayout(layout)

    def update_status(self, button, name):
        """Update the status panel when a button is clicked."""
        status = "off" if button.led_on else "on"
        self.status_label.setText(f"Motor: {name} button is {status}")

    def dial_value_changed(self):
        """Update the status panel with the current dial value."""
        value = self.dial.value()
        self.status_label.setText(f"Motor Speed - {value}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LEDButtonPanel()
    window.show()
    sys.exit(app.exec_())
