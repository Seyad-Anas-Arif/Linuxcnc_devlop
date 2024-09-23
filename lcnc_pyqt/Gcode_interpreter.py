import math
class GCodeInterpreter:
    def __init__(self):
        self.position = {'X': 0, 'Y': 0, 'Z': 0}  # Current position of the tool
        self.feed_rate = 1000  # Default feed rate
        self.unit = 'mm'  # Default unit (can be 'mm' or 'inches')

    def parse_gcode(self, gcode_file):
        """Reads the G-code file and executes commands line by line."""
        with open(gcode_file, 'r') as file:
            for line in file:
                # Remove comments (everything after ';')
                command = line.split(';')[0].strip()
                
                if command:  # Skip empty lines
                    print(f"Processing command: {command}")
                    self.process_command(command)
    
    def process_command(self, command):
        """Processes individual G-code commands."""
        tokens = command.split()
        g_command = tokens[0]
        
        if g_command == 'G0' or g_command == 'G1':  # Linear motion
            self.linear_move(tokens)
        elif g_command == 'G2' or g_command == 'G3':  # Arc motion
            self.arc_move(tokens, clockwise=(g_command == 'G2'))
        elif g_command.startswith('G'):  # Handle other G commands
            self.other_gcode_commands(g_command, tokens)
        elif g_command.startswith('M'):  # Handle M codes (Machine specific)
            self.machine_commands(g_command)
        else:
            print(f"Unknown command: {g_command}")
    
    def linear_move(self, tokens):
        """Handles G0 (rapid move) and G1 (linear move) commands."""
        new_position = self.position.copy()  # Start with current position

        for token in tokens[1:]:
            axis = token[0]
            value = float(token[1:])  # This is where the error happened

            if axis in new_position:
                new_position[axis] = value
        
        # Output the calculated new position and feed rate
        print(f"Moving to {new_position} with feed rate {self.feed_rate} {self.unit}/min")
        self.position = new_position
    
    def arc_move(self, tokens, clockwise=True):
        """Handles G2 (clockwise arc) and G3 (counterclockwise arc)."""
        center_offset = {'I': 0, 'J': 0}
        radius = 0
        new_position = self.position.copy()

        for token in tokens[1:]:
            axis = token[0]
            value = float(token[1:])
            if axis in new_position:
                new_position[axis] = value
            elif axis in center_offset:
                center_offset[axis] = value
        
        # Calculate arc trajectory (simplified) and print the action
        radius = math.sqrt(center_offset['I']**2 + center_offset['J']**2)
        direction = "clockwise" if clockwise else "counterclockwise"
        print(f"Moving in an arc to {new_position} with radius {radius} in {direction} direction")

        self.position = new_position

    def other_gcode_commands(self, g_command, tokens):
        """Handles additional G-code commands like units and feed rates."""
        if g_command == 'G20':  # Set units to inches
            self.unit = 'inches'
            print("Units set to inches.")
        elif g_command == 'G21':  # Set units to millimeters
            self.unit = 'mm'
            print("Units set to millimeters.")
        elif g_command == 'G90':  # Absolute positioning
            print("Set to absolute positioning.")
        elif g_command == 'G91':  # Incremental positioning
            print("Set to incremental positioning.")
        else:
            print(f"Unhandled G-command: {g_command}")
    
    def machine_commands(self, m_command):
        """Processes M-codes (e.g., spindle control, coolant)."""
        if m_command == 'M3':
            print("Spindle on (clockwise).")
        elif m_command == 'M4':
            print("Spindle on (counterclockwise).")
        elif m_command == 'M5':
            print("Spindle stop.")
        elif m_command == 'M30':
            print("Program end.")
        else:
            print(f"Unhandled M-command: {m_command}")

if __name__ == "__main__":
    # Create the GCodeInterpreter instance
    interpreter = GCodeInterpreter()
    
    # Path to a G-code file
    gcode_file = 'test.ngc'
    
    # Parse and interpret the G-code file
    interpreter.parse_gcode(gcode_file)
