import tkinter as tk
import tkinter.font as tkfont

window = tk.Tk()

##### VARIABLES #####
black = "#000000"
dark_gray = "#37353E"
light_gray = "#44444E"
brown = "#715A5A"
white = "#D3DAD9"
consolas = tkfont.Font(family="Consolas", size=12)
current_tab = "CPU_code"

instructions = [
    "NOP",
    "HLT",
    "NOT",
    "ADD",
    "SUB",
    "AND",
    "XOR",
    "NOR",
    "RSH",
    "LDI",
    "ADI",
    "LOD",
    "STR",
    "REQ",
    "OUT",
    "CAL",
    "RET",
    "BRH",
    "RNG"
]

##### WINDOW INITIALIZATION #####
window.geometry("1280x720")
window.title("CiS Emulator")
window.configure(bg=dark_gray)

##### FRAMES #####
CPU_frame = tk.Frame(window, bg=dark_gray)
CPU_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
CPU_frame.pack_propagate(False)

IO_frame = tk.Frame(window, bg=light_gray)
IO_frame.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
IO_frame.pack_propagate(False)

##### TABS #####
CPU_tabs = tk.Frame(CPU_frame, bg=dark_gray)
CPU_tabs.pack(side="top", fill="x")

CPU_code = tk.Button(CPU_tabs, text="Code", bg=white, fg=black, font=consolas)
CPU_code.pack(side="left", fill="x", expand=True)

CPU_registers = tk.Button(CPU_tabs, text="Registers", bg=white, fg=black, font=consolas)
CPU_registers.pack(side="left", fill="x", expand=True)

CPU_ram = tk.Button(CPU_tabs, text="RAM", bg=white, fg=black, font=consolas)
CPU_ram.pack(side="left", fill="x", expand=True)

#===== CPU CODE TAB =====#
if current_tab == "CPU_code":
    CPU_code_content = tk.Text(CPU_frame, bg=dark_gray, fg="#D4D4D4", font=consolas)
    CPU_code_content.pack(side="top", fill="both", expand=True)

    # Colors for syntax highlighting
    CPU_code_content.tag_configure("opcode", foreground="#569CD6")
    CPU_code_content.tag_configure("register", foreground="#4EC9B0")
    CPU_code_content.tag_configure("immediate", foreground="#B5CEA8")
    CPU_code_content.tag_configure("comment", foreground="#6A9955")
    CPU_code_content.tag_configure("label", foreground="#C586C0")
    CPU_code_content.tag_configure("default", foreground="#D4D4D4")

def syntax_highlighting():
    CPU_code_content_text = CPU_code_content.get("1.0", tk.END)
    pass

while True:
    syntax_highlighting()
    window.update_idletasks()
    window.update()