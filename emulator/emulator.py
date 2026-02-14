import re
import tkinter as tk
from tkinter import ttk
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
    "HLT", "HALT", # both of these works
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
    "CAL", "CALL", # both of these works
    "RET",
    "BRH",
    "RNG"
]

flags = [
    "JMP",
    "ZERO",
    "!ZERO",
    "COUT",
    "!COUT",
    "MSB",
    "!MSB",
    "LSB"
]

registers = {f"r{i+1}": 0 for i in range(7)}
ram = {f"[{i}]": 0 for i in range(64)}
code = "; Insert your assembly code for CiS here!" # The code in the program

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

def update_current_tab(tab):
    global current_tab
    current_tab = tab
    update_tabs_on_screen()

CPU_tabs = tk.Frame(CPU_frame, bg=dark_gray)
CPU_tabs.pack(side="top", fill="x")

CPU_code = tk.Button(CPU_tabs, text="Code", bg=white, fg=black, font=consolas, command=lambda: update_current_tab("CPU_code"), bd=0)
CPU_code.pack(side="left", fill="x", expand=True)

CPU_memory = tk.Button(CPU_tabs, text="Memory", bg=white, fg=black, font=consolas, command=lambda: update_current_tab("CPU_memory"), bd=0)
CPU_memory.pack(side="left", fill="x", expand=True)

CPU_settings = tk.Button(CPU_tabs, text="Settings", bg=white, fg=black, font=consolas, command=lambda: update_current_tab("CPU_settings"), bd=0)
CPU_settings.pack(side="left", fill="x", expand=True)

#===== TABS =====#
def update_memory():
    # If the current tab isnt CPU_memory then return
    if current_tab != "CPU_memory":
        return
    
    # Destroy all the widgets
    for widget in register_frame.winfo_children():
        widget.destroy()
    for widget in ram_frame.winfo_children():
        widget.destroy()

    # Create the labels
    for reg in registers:
        reg_label = tk.Label(register_frame, text=f"{reg}: {registers[reg]}", bg=brown, fg=white, font=consolas, anchor="w")
        reg_label.pack(side="top", fill="x")
    for ram_index in ram:
        ram_label = tk.Label(ram_frame, text=f"{ram_index}: {ram[ram_index]}", bg=dark_gray, fg=white, font=consolas, anchor="w")
        ram_label.pack(side="top", fill="x")

    window.after(100, update_memory)

def update_tabs_on_screen():
    global registers
    # Destroy all the widgets
    for widget in CPU_frame.winfo_children():
        if widget not in [CPU_tabs]:
            widget.destroy()
    
    CPU_code.configure(bg=white, fg=black)
    CPU_memory.configure(bg=white, fg=black)
    CPU_settings.configure(bg=white, fg=black)

    if current_tab == "CPU_code":
        global CPU_code_content

        # Change button color
        CPU_code.configure(bg=black, fg=white)

        CPU_code_run = tk.Button(CPU_frame, text="Run Code", bg=white, fg=black, font=consolas, bd=0)
        CPU_code_run.pack(side="top", fill="x")

        CPU_code_content = tk.Text(CPU_frame, bg=dark_gray, fg="#D4D4D4", font=consolas, bd=0)
        CPU_code_content.pack(side="top", fill="both", expand=True)

        # After each key release save the code
        def save_code(event):
            global code
            code = CPU_code_content.get("1.0", tk.END)

        CPU_code_content.bind("<KeyRelease>", save_code)
        CPU_code_content.bind("<KeyRelease>", syntax_highlighting)

        # Placeholder text
        CPU_code_content.insert("1.0", code)
        syntax_highlighting()

        # Colors for syntax highlighting (got this from chatgpt aswell and edited it a bit :3)
        CPU_code_content.tag_configure("opcode", foreground="#569CD6")
        CPU_code_content.tag_configure("register", foreground="#4EC9B0")
        CPU_code_content.tag_configure("ram", foreground="#CE9178")
        CPU_code_content.tag_configure("immediate", foreground="#B5CEA8")
        CPU_code_content.tag_configure("comment", foreground="#6A9955")
        CPU_code_content.tag_configure("label", foreground="#C586C0")
        CPU_code_content.tag_configure("default", foreground="#D4D4D4")
        CPU_code_content.tag_configure("flag", foreground="#EBEB99")
    elif current_tab == "CPU_memory":
        # Mostly gets handled by update_memory()
        global register_frame, ram_frame

        # Change button color
        CPU_memory.configure(bg=black, fg=white)

        # Make frames and make ram scrollable

        # Add the titles to here
        reg_title = tk.Label(CPU_frame, text="Registers", bg=black, fg=white, font=consolas)
        reg_title.pack(side="top", fill="x")

        register_frame = tk.Frame(CPU_frame, bg=dark_gray)
        register_frame.pack(side="top", fill="x")
        
        ram_title = tk.Label(CPU_frame, text="RAM", bg=black, fg=white, font=consolas)
        ram_title.pack(side="top", fill="x")
        
        parent_ram_canvas = tk.Canvas(CPU_frame, bg=dark_gray, highlightthickness=0, bd=0)
        parent_ram_canvas.pack(side="left", fill="both", expand=True)
        ram_scrollbar = ttk.Scrollbar(parent_ram_canvas, orient="vertical", command=parent_ram_canvas.yview)
        ram_scrollbar.pack(side="right", fill="y")

        ram_frame = tk.Frame(parent_ram_canvas, bg=dark_gray, bd=0)
        ram_frame.bind("<Configure>", lambda e: parent_ram_canvas.configure(yscrollcommand=ram_scrollbar.set, scrollregion=parent_ram_canvas.bbox("all")))

        center_y = ram_frame.winfo_screenheight() / 2
        parent_ram_canvas.create_window((0, center_y), window=ram_frame, anchor="n")

        def on_mouse_wheel(event):
            parent_ram_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
        parent_ram_canvas.bind_all("<MouseWheel>", on_mouse_wheel)
        
        update_memory()

    elif current_tab == "CPU_settings":
        # Change button color
        CPU_settings.configure(bg=black, fg=white)

#===== CPU CODE TAB =====#
# i used chatgpt for this
def syntax_highlighting(event = None):
    # If current tab isn't code then break
    if current_tab != "CPU_code":
        return

    # Save current selection
    try:
        selection_start = CPU_code_content.index("sel.first")
        selection_end = CPU_code_content.index("sel.last")
    except tk.TclError:
        selection_start = None
        selection_end = None
    
    cursor_pos = CPU_code_content.index("insert")

    # Remove tags
    for tag in CPU_code_content.tag_names():
        CPU_code_content.tag_remove(tag, "1.0", tk.END)

    # Restore selection
    if selection_start and selection_end:
        CPU_code_content.tag_add("sel", selection_start, selection_end)

    # Restore cursor
    CPU_code_content.mark_set("insert", cursor_pos)

    # Get the code text and split into lines
    CPU_code_content_text = CPU_code_content.get("1.0", tk.END)
    CPU_code_content_text_lines = CPU_code_content_text.splitlines()

    for line_idx, line in enumerate(CPU_code_content_text_lines):
        # Current column
        cur_col = 0

        # Get the words in the line
        words = line.split()

        for word in words:
            start_col = line.find(word, cur_col)
            end_col = start_col + len(word)

            start_index = f"{line_idx + 1}.{start_col}"
            end_index = f"{line_idx + 1}.{end_col}"

            # Check if the word is a comment
            if word[0] == ";":
                CPU_code_content.tag_add("comment", start_index, f"{line_idx + 1}.end")
                break

            # === These checks are for words that are only able to be written once in a line, so we don't need to check them with regex
            # If word is instruction
            if word.upper() in instructions:
                CPU_code_content.tag_add("opcode", start_index, end_index)
            
            # If word is an immediate
            elif word[:2] == "0d" or word[:2] == "0b" or word[:2] == "0x":
                CPU_code_content.tag_add("immediate", start_index, end_index)
            
            # If word is a flag
            elif word.upper() in flags:
                CPU_code_content.tag_add("flag", start_index, end_index)
            
            # If word is a label
            elif word[0] == ".":
                CPU_code_content.tag_add("label", start_index, end_index)
            
            # If word is a RAM
            elif word[0] == "[" and word[-1] == "]":
                CPU_code_content.tag_add("ram", start_index, end_index)

            # For registers
            for match in re.finditer(r"\br\d+\b", line, re.IGNORECASE):
                start = f"{line_idx + 1}.{match.start()}"
                end = f"{line_idx + 1}.{match.end()}"

                CPU_code_content.tag_add("register", start, end)
            
            col = end_col  # move forward so duplicates work correctly

update_tabs_on_screen()
syntax_highlighting()
window.mainloop()