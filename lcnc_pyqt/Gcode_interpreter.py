import re

class GCodeInterpreter:
    def __init__(self):
        self.position = {'X': 0.0, 'Y': 0.0, 'Z': 0.0}
        self.feed_rate = 1000  # Default feed rate in mm/min

    def execute_command(self, command):
        command = command.strip()
        if not command or command.startswith(';'):
            # Ignore empty lines or comments
            return
        
        # Parse the command
        match = re.match(r'([G|M|T|S]\d+)(.*)', command)
        if not match:
            print(f"Unrecognized command: {command}")
            return

        code, params = match.groups()
        params = params.strip()

        if code.startswith('G'):
            self.execute_g_command(code, params)
        elif code.startswith('M'):
            self.execute_m_command(code, params)
        else:
            print(f"Unrecognized code: {code}")

    def execute_g_command(self, code, params):
        if code == 'G0' or code == 'G1':
            self.move(params)
        else:
            print(f"Unsupported G-code command: {code}")

    def execute_m_command(self, code, params):
        if code == 'M30':
            print("End of program")
        else:
            print(f"Unsupported M-code command: {code}")

    def move(self, params):
        moves = re.findall(r'[XYZ]\s*(-?\d+\.?\d*)', params)
        for axis, value in zip('XYZ', moves):
            if value:
                self.position[axis] = float(value)
        print(f"Moved to position: {self.position}")

# Example usage
gcode = [
"G21",
"G17",       
"G90",        

"G0 X0 Y0",
"G2 X1 Y1 I1"
"M3 S1000 ",
"G1 X50 Y0 F1000", 
"G1 X50 Y50",      
"G1 X0 Y50",      
"G1 X0 Y0",     
"M5",      
"G0 X0 Y0",  
"M30"       

]

interpreter = GCodeInterpreter()
for line in gcode:
    interpreter.execute_command(line)
