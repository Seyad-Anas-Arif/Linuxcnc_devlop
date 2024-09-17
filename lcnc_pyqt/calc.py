import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLineEdit, QVBoxLayout, QGridLayout

class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        
        # Window settings
        self.setWindowTitle("Simple Calculator")
        self.setGeometry(100, 100, 400, 400)
        
        # Create the display for the calculator
        self.display = QLineEdit(self)
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        
        # Create buttons and layout
        self.create_buttons()
        
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)
        main_layout.addLayout(self.button_layout)
        
        self.setLayout(main_layout)
    
    def create_buttons(self):
        """Create the calculator buttons and their layout."""
        self.button_layout = QGridLayout()
        
        # Button text and positions
        buttons = {
            '7': (0, 0), '8': (0, 1), '9': (0, 2), '/': (0, 3),
            '4': (1, 0), '5': (1, 1), '6': (1, 2), '*': (1, 3),
            '1': (2, 0), '2': (2, 1), '3': (2, 2), '-': (2, 3),
            '0': (3, 0), 'C': (3, 1), '=': (3, 2), '+': (3, 3)
        }
        
        # Create each button and connect it to the click handler
        for button_text, pos in buttons.items():
            button = QPushButton(button_text)
            button.setFixedSize(80, 80)
            self.button_layout.addWidget(button, pos[0], pos[1])
            button.clicked.connect(lambda _, b=button_text: self.on_button_click(b))
    
    def on_button_click(self, button_text):
        """Handle button click event."""
        current_text = self.display.text()
        
        if button_text == 'C':  # Clear the display
            self.display.clear()
        elif button_text == '=':  # Evaluate the expression
            try:
                result = eval(current_text)  # Evaluate the expression
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        else:  # For numbers and operators, add to the display
            self.display.setText(current_text + button_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
