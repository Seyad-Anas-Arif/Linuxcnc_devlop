import os
import re
import shutil
import select
import subprocess
import sys
import time
import linuxcnc

# Define Dummy classes
class DummyCanon:
    pass

class Progress:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def set_text(self, text):
        print(text)

    def update(self, progress, step=1):
        print(f"Progress: {progress}/{self.end}")

    def nextphase(self, steps):
        print(f"Next phase: {steps}")

    def done(self):
        print("Done")

class AxisCanon:
    def __init__(self, o, widgets_text, i, progress, arcdivision):
        pass

class DummyProgress:
    pass

# Regex to match filter progress
progress_re = re.compile("^FILTER_PROGRESS=(\\d*)$")

# Function to parse G-Code expression
def parse_gcode_expression(e):
    f = os.path.devnull
    canon = DummyCanon()

    parameter = inifile.find("RS274NGC", "PARAMETER_FILE")
    temp_parameter = os.path.join(tempdir, os.path.basename(parameter))
    shutil.copy(parameter, temp_parameter)
    canon.parameter_file = temp_parameter

    result, seq = gcode.parse("", canon, "M199 P["+e+"]", "M2")
    if result > gcode.MIN_ERROR: 
        return False, gcode.strerror(result)
    
    return True, canon.number

# Function to filter a program file
def filter_program(program_filter, infilename, outfilename):
    outfile = open(outfilename, "w")
    infilename_q = infilename.replace("'", "'\\''")
    env = dict(os.environ)
    env['AXIS_PROGRESS_BAR'] = '1'

    p = subprocess.Popen(["sh", "-c", "%s '%s'" % (program_filter, infilename_q)],
                          stdin=subprocess.PIPE,
                          stdout=outfile,
                          stderr=subprocess.PIPE,
                          env=env)
    p.stdin.close()
    progress = Progress(1, 100)
    progress.set_text("Filtering...")
    stderr_text = []

    try:
        while p.poll() is None:
            r, w, x = select.select([p.stderr], [], [], 0.100)
            if r:
                stderr_line = p.stderr.readline().decode()
                m = progress_re.match(stderr_line)
                if m:
                    progress.update(int(m.group(1)), 1)
                else:
                    stderr_text.append(stderr_line)
                    sys.stderr.write(stderr_line)
        
        for line in p.stderr:
            stderr_line = line.decode()
            m = progress_re.match(stderr_line)
            if not m:
                stderr_text.append(stderr_line)
                sys.stderr.write(stderr_line)

        return p.returncode, "".join(stderr_text)
    
    finally:
        progress.done()

# Function to retrieve the filter for a given file
def get_filter(filename):
    ext = os.path.splitext(filename)[1]
    if ext:
        return inifile.find("FILTER", ext[1:])
    else:
        return None

# Function to reload a file
def reload_file(refilter=True):
    if running(): 
        return
    
    s.poll()

    if not loaded_file:
        root_window.tk.call("set_mode_from_tab")
        return
    
    line = vars.highlight_line.get()
    o.set_highlight_line(None)

    if refilter or not get_filter(loaded_file):
        tempfile = os.path.join(tempdir, os.path.basename(loaded_file))
        shutil.copyfile(loaded_file, tempfile)
        open_file_guts(tempfile, False, False)
    else:
        tempfile = os.path.join(tempdir, "filtered-" + os.path.basename(loaded_file))
        open_file_guts(tempfile, True, False)
    
    if line:
        o.set_highlight_line(line)

# Core function to open a file with LinuxCNC and process it
def open_file_guts(f, filtered=False, addrecent=True):
    s.poll()
    save_task_mode = s.task_mode
    ensure_mode(linuxcnc.MODE_MANUAL)
    
    if addrecent:
        add_recent_file(f)
    
    if not filtered:
        program_filter = get_filter(f)
        if program_filter:
            tempfile = os.path.join(tempdir, "filtered-" + os.path.basename(f))
            exitcode, stderr = filter_program(program_filter, f, tempfile)
            if exitcode:
                root_window.tk.call("nf_dialog", (".error", "-ext", stderr),
                        "Filter failed",
                        "The program %(program)r exited with code %(code)d. Any error messages it produced are shown below:"
                        % {'program': program_filter, 'code': exitcode},
                        "error", 0, "OK")
                return
            ensure_mode(save_task_mode)
            return open_file_guts(tempfile, True, False)
    
    ensure_mode(save_task_mode)
    set_first_line(0)
    t0 = time.time()

    canon = None
    o.deselect(None)

    try:
        c.task_plan_synch()
        c.wait_complete()
        c.program_open(f)
        lines = open(f).readlines()
        progress = Progress(2, len(lines))
        t.configure(state="normal")
        t.tk.call("delete_all", t)

        code = []
        for i, l in enumerate(lines):
            l = l.expandtabs().replace("\r", "")
            code.extend([f"{i+1:6}: ", "lineno", l, ""])
            if i % 1000 == 0:
                t.insert("end", *code)
                del code[:]
                progress.update(i)
        
        if code:
            t.insert("end", *code)
        
        progress.nextphase(len(lines))
        f = os.path.abspath(f)
        o.canon = canon = AxisCanon(o, widgets.text, i, progress, arcdivision)
        root_window.bind_class(".info.progress", "<Escape>", cancel_open)

        parameter = inifile.find("RS274NGC", "PARAMETER_FILE")
        temp_parameter = os.path.join(tempdir, os.path.basename(parameter))
        if os.path.exists(parameter):
            shutil.copy(parameter, temp_parameter)
        
        canon.parameter_file = temp_parameter

        timeout = inifile.find("DISPLAY", "PREVIEW_TIMEOUT") or ""
        if timeout:
            canon.set_timeout(float(timeout))

        initcode = inifile.find("EMC", "RS274NGC_STARTUP_CODE") or ""
        if initcode == "":
            initcode = inifile.find("RS274NGC", "RS274NGC_STARTUP_CODE") or ""

        initcodes = []
        if initcode:
            initcodes.append(initcode)
        
        unitcode = f"G{20 + (s.linear_units == 1)}"
        initcodes.append(unitcode)
        initcodes.append("g90")
        initcodes.append(f"t{s.tool_in_spindle} m6")
        
        for i in range(9):
            if s.axis_mask & (1 << i):
                axis = "XYZABCUVW"[i]
                pos = s.position[i] % 360.000 if axis in "ABC" else s.position[i]
                position = f"g53 g0 {axis}{pos:.8f}"
                initcodes.append(position)

        try:
            result, seq = o.load_preview(f, canon, initcodes, interpname)
        except KeyboardInterrupt:
            result, seq = 0, 0

        if result > gcode.MIN_ERROR:
            error_str = gcode.strerror(result)
            root_window.tk.call("nf_dialog", ".error",
                                f"G-Code error in {os.path.basename(f)}",
                                f"Near line {seq} of {f}:\n{error_str}",
                                "error", 0, "OK")

        t.configure(state="disabled")
        o.lp.set_depth(from_internal_linear_unit(o.get_foam_z()),
                       from_internal_linear_unit(o.get_foam_w()))

    except Exception as e:
        notifications.add("error", str(e))
    
    finally:
        root_window.update()
        root_window.tk.call("destroy", ".info.progress")
        root_window.tk.call("grab", "release", ".info.progress")
        if canon:
            canon.progress = DummyProgress()
        try:
            progress.done()
        except UnboundLocalError:
            pass
        o.tkRedraw()
        root_window.tk.call("set_mode_from_tab")

# Additional utility functions
def interp_statename(x):
    if x == linuxcnc.INTERP_IDLE: return "IDLE"
    if x == linuxcnc.INTERP_READING: return "READING"
    if x == linuxcnc.INTERP_PAUSED: return "PAUSED"
    if x == linuxcnc.INTERP_WAITING: return "WAITING"

def motion_modename(x):
    if x == linuxcnc.TRAJ_MODE_FREE: return "FREE"
    if x == linuxcnc.TRAJ_MODE_COORD: return "COORD"
    if x == linuxcnc.TRAJ_MODE_TELEOP: return "TELEOP"

def task_modename(x):
    if x == linuxcnc.MODE_MDI: return "MDI"
    if x == linuxcnc.MODE_MANUAL: return "MANUAL"
    if x == linuxcnc.MODE_AUTO: return "AUTO"
