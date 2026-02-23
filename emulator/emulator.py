"""
TODO: Add ports and I/O functions, add settings and memory tab, and add the assembly thigny
"""

#========== Imports ==========#
import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from tkinter import filedialog

#========== Initializations ==========#
window = tk.Tk()

#========== Classes ==========#

#========== Variables ==========#

# Colors
black = "#000000"
dark_gray = "#37353E"
light_gray = "#44444E"
brown = "#715A5A"
white = "#D3DAD9"

# Code colors
code_color_bg = "#1E1E1E"
code_color_fg = "#D4D4D4"
code_color_opcode = "#569CD6"
code_color_register = "#4EC9B0"
code_color_ram = "#CE9178"
code_color_immediate = "#B5CEA8"
code_color_comment = "#6A9955"
code_color_label = "#C586C0"
code_color_flag = "#EBEB99"
code_color_port = "#9CDCFE"
code_color_error = "#F14C4C"

# Fonts
consolas = tkfont.Font(family="Consolas", size=12)

# Other variables
current_tab = "CPU_code"
saved = False # See if the code in the textbox is saved
save_file = ""

opcodes = [
    "NOP",
    "HALT", "HLT", # aliases
    "NOT",
    "ADD",
    "SUB",
    "AND",
    "XOR",
    "NOR",
    "RSH",
    "LDI",
    "ADI",
    "LFR",
    "STR",
    "REQ",
    "OUT",
    "CALL", "CAL", # aliases
    "RET",
    "BRH",
    "RNG"
]

flags = [
    "JMP", "TRUE", # aliases
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
ports = {f"p{i}": 0 for i in range(4)}
call_stack = ["" for i in range(8)]
code = "; Insert your assembly code for CiS here!" # The code in the program

#========== Window configurations ==========#
window.geometry("1280x720")
window.title("CiS Emulator - Untitled")
window.configure(bg=dark_gray)

#========== Frames & Tabs ==========#

# Main CPU functions
CPU_frame = tk.Frame(window, bg=dark_gray)
CPU_frame.pack(side="left", fill="both", expand=True)
CPU_frame.pack_propagate(False)

# The I/O functions
IO_frame = tk.Frame(window, bg=light_gray)
IO_frame.pack(side="left", fill="both", expand=True)
IO_frame.pack_propagate(False)

# The CPU tabs
CPU_tabs = tk.Frame(CPU_frame, bg=dark_gray)
CPU_tabs.pack(side="top", fill="x")

# Code tab - where the user can write code or import code
CPU_code = tk.Button(CPU_tabs, text="Code", bg=white, fg=black, font=consolas, command=lambda: update_tabs_on_screen("CPU_code"), bd=0)
CPU_code.pack(side="left", fill="x", expand=True)

# Memory tab - where the user can see the registers, ram and call stack
CPU_memory = tk.Button(CPU_tabs, text="Memory", bg=white, fg=black, font=consolas, command=lambda: update_tabs_on_screen("CPU_memory"), bd=0)
CPU_memory.pack(side="left", fill="x", expand=True)

# Settings tab - where the user can change the settings of the CPU e.g. the clock speed
CPU_settings = tk.Button(CPU_tabs, text="Settings", bg=white, fg=black, font=consolas, command=lambda: update_tabs_on_screen("CPU_settings"), bd=0)
CPU_settings.pack(side="left", fill="x", expand=True)

# update_tabs_on_screen() is called to update the widgets that is being shown on the screen
def update_tabs_on_screen(tab):

    # Update the current tab variable
    global current_tab
    current_tab = tab

    # Destroy all the current widgets on screen to replace them
    for widget in CPU_frame.winfo_children():
        # If the widget isn't the CPU tabs, destroy it
        if widget != CPU_tabs:
            widget.destroy()
    
    # Reset the CPU tab buttons
    for tab in CPU_tabs.winfo_children():
        tab.configure(bg=white, fg=black)
    
    # Switch between the tabs
    match current_tab:

        # Code tab - all variables here and functions should start with "CPU_code"
        case "CPU_code":
            # Global variables
            global CPU_code_textbox

            # Change the button color
            CPU_code.configure(bg=black, fg=white)

            # Run button - runs the current program in the textbox
            CPU_code_run = tk.Button(CPU_frame, text="Run Code", bg=white, fg=black, font=consolas, bd=0)
            CPU_code_run.pack(side="top", fill="x")

            # Import button - imports a .cis file and puts the code into the textbox
            CPU_code_import = tk.Button(CPU_frame, text="Import Code", bg=white, fg=black, font=consolas, bd=0, command=import_code)
            CPU_code_import.pack(side="top", fill="x")

            # Save button - saves the code in the textbox to a .txt file or to the current file that was imported/saved to
            CPU_code_save = tk.Button(CPU_frame, text="Save Code", bg=white, fg=black, font=consolas, bd=0, command=lambda: save_code("current"))
            CPU_code_save.pack(side="top", fill="x")

            # Save As button - saves the code in the textbox to a .txt file but as a different file
            CPU_code_save = tk.Button(CPU_frame, text="Save Code As", bg=white, fg=black, font=consolas, bd=0, command=save_code)
            CPU_code_save.pack(side="top", fill="x")

            # Textbox - where people can write code and run/save it
            CPU_code_textbox = tk.Text(CPU_frame, bg=code_color_bg, fg=code_color_fg, font=consolas, insertbackground=code_color_fg, bd=0)
            CPU_code_textbox.pack(side="top", fill="both", expand=True)

            # Create tags for the syntax highlighting
            CPU_code_textbox.tag_configure("opcode", foreground=code_color_opcode)
            CPU_code_textbox.tag_configure("register", foreground=code_color_register)
            CPU_code_textbox.tag_configure("ram", foreground=code_color_ram)
            CPU_code_textbox.tag_configure("immediate", foreground=code_color_immediate)
            CPU_code_textbox.tag_configure("comment", foreground=code_color_comment)
            CPU_code_textbox.tag_configure("label", foreground=code_color_label)
            CPU_code_textbox.tag_configure("flag", foreground=code_color_flag)
            CPU_code_textbox.tag_configure("port", foreground=code_color_port)
            CPU_code_textbox.tag_configure("error", underline=True, underlinefg=code_color_error)

            # CPU_code_save_code() is called to save the code in the textbox to the code variable
            def CPU_code_save_code(event):
                global code
                code = CPU_code_textbox.get("1.0", "end")
                
                # If the save_file is empty, make the title Untitled
                if not save_file:
                    window.title(f"CiS Emulator - Untitled*")
                
                # Otherwise make it the file path
                else:
                    window.title(f"CiS Emulator - {save_file}*")
            
            # Binding
            CPU_code_textbox.bind("<KeyRelease>", CPU_code_save_code, add="+")
            CPU_code_textbox.bind("<KeyRelease>", syntax_highlighting, add="+")
            # If the text is pasted it wont update
            CPU_code_textbox.bind("<<Paste>>", lambda e: window.after(1, lambda: syntax_highlighting(True)), add="+")

            # Load the code variable into the textbox
            CPU_code_textbox.insert("1.0", code)
            syntax_highlighting(True) # Call syntax_highlighting() since the text won't get updated automatically

        # Memory tab - displays the current values in registers, ram and the call stack
        case "CPU_memory":
            # Global variables
            global registers_frame, ram_frame, call_stack_frame

            # Change the button color
            CPU_memory.configure(bg=black, fg=white)

            # Create the registers, ram and call stack labels and frames
            registers_label = tk.Label(CPU_frame, text="Registers", bg=dark_gray, fg=white, font=consolas)
            registers_frame = tk.Frame(CPU_frame, bg=dark_gray)
            registers_label.pack(side="top", fill="x")
            registers_frame.pack(side="top", fill="x")


            # The ram frame is too small, so we make it scrollable
            # The label
            ram_label = tk.Label(CPU_frame, text="RAM", bg=light_gray, fg=white, font=consolas)
            ram_label.pack(side="top", fill="x")
            
            # The parent ram to store the canvas
            # Height must be preset so no bleeding occurs
            ram_canvas_container = tk.Frame(CPU_frame, height=200)
            ram_canvas_container.pack_propagate(False)
            ram_canvas_container.pack(side="top", fill="both", expand=True)

            # The canvas (for the frame and scrollbar)
            parent_ram_canvas = tk.Canvas(ram_canvas_container, bg=light_gray, highlightthickness=0, bd=0)
            parent_ram_canvas.pack(side="top", fill="both", expand=True)

            # The scrollbar
            ram_scrollbar = ttk.Scrollbar(parent_ram_canvas, orient="vertical", command=parent_ram_canvas.yview)
            ram_scrollbar.pack(side="right", fill="y")

            # The actual frame
            ram_frame = tk.Frame(parent_ram_canvas, bg=dark_gray, bd=0)
            ram_frame.bind("<Configure>", lambda e: parent_ram_canvas.configure(yscrollcommand=ram_scrollbar.set, scrollregion=parent_ram_canvas.bbox("all")))

            # Create the frame in the canvas
            parent_ram_canvas.create_window((0, 0), window=ram_frame, anchor="nw")

            # Mouse scrolling function
            def mouse_scrolling(event):
                parent_ram_canvas.yview_scroll(-1 * int((event.delta / 120)), "units")
            
            # Make the frame scrollable
            parent_ram_canvas.bind("<Enter>", lambda e: parent_ram_canvas.bind_all("<MouseWheel>", mouse_scrolling))
            parent_ram_canvas.bind("<Leave>", lambda e: parent_ram_canvas.unbind_all("<MouseWheel>"))


            # Back to the call stack
            call_stack_label = tk.Label(CPU_frame, text="Call Stack", bg=dark_gray, fg=white, font=consolas)
            call_stack_frame = tk.Frame(CPU_frame, bg=dark_gray)
            call_stack_label.pack(side="top", fill="x")
            call_stack_frame.pack(side="top", fill="x")

            update_memory()
        
        # Settings tab - the settings of the CPU
        case "CPU_settings":
            # Change the button color
            CPU_settings.configure(bg=black, fg=white)


#========== Other Functions ==========#

# syntax_highlighting(all) is called to update the colors of the code in the textbox
# If all is true, it will update the colors on every line
def syntax_highlighting(all=False):
    # If the current tab isn't the code tab, return
    if current_tab != "CPU_code":
        return
    
    # Save the current selection (if there is one) and cursor
    try:
        selection_start = CPU_code_textbox.index("sel.first")
        selection_end = CPU_code_textbox.index("sel.last")
    except tk.TclError:
        selection_start = None
        selection_end = None
    cursor_pos = CPU_code_textbox.index("insert")

    # syntax_line(line, line_index) is called to update only one line
    def syntax_line(line, line_index):
        # Current column
        cur_col = 0

        # Get the words in the line
        words = line.split()

        for word in words:
            # Get the column of the start of the word and the end of the word
            start_col = line.find(word, cur_col)
            end_col = start_col + len(word)

            # Get the index of the start and end of the word using the line index
            start_index = f"{line_index + 1}.{start_col}"
            end_index = f"{line_index + 1}.{end_col}"

            # If the word is a comment, color the comment with the comment tag and break
            if word[0] == ";":
                CPU_code_textbox.tag_add("comment", start_index, f"{line_index + 1}.end") # Color the entire line
                break

            # If the word is an opcode
            if word.upper() in opcodes:
                CPU_code_textbox.tag_add("opcode", start_index, end_index)
            
            # If the word is an immediate
            elif word[:2] == "0x" or word[:2] == "0b" or word[:2] == "0d" or word.isdigit():
                CPU_code_textbox.tag_add("immediate", start_index, end_index)
            
            # If the word is a flag
            elif word.upper() in flags:
                CPU_code_textbox.tag_add("flag", start_index, end_index)
            
            # If the word is RAM
            elif word[0] == "[" and word[-1] == "]":
                CPU_code_textbox.tag_add("ram", start_index, end_index)
            
            # If the word is a register
            elif word.lower() in registers or word.lower() == "r0": # Special case since r0 can't be written to
                CPU_code_textbox.tag_add("register", start_index, end_index)
            
            # If the word is a label
            elif word[0] == ".":
                CPU_code_textbox.tag_add("label", start_index, end_index)
            
            # If the word is a port
            elif word.lower() in ports:
                CPU_code_textbox.tag_add("port", start_index, end_index)
            
            # Otherwise, it's an error
            else:
                CPU_code_textbox.tag_add("error", start_index, end_index)
            
            cur_col = end_col # Move the current column to the end of the word so that duplicates work correctly

    # If all is true, reset everything
    if all:
        # Remove all tags
        for tag in CPU_code_textbox.tag_names():
            CPU_code_textbox.tag_remove(tag, "1.0", "end")
        
        # Split the code into lines and update each seperately
        lines = CPU_code_textbox.get("1.0", "end").splitlines()
        for line_idx, line in enumerate(lines):
            syntax_line(line, line_idx)
    
    # Otherwise, only reset the current line
    else:
        # Get the current line index
        line_index = int(CPU_code_textbox.index("insert").split(".")[0]) - 1

        # Get the current line
        line = CPU_code_textbox.get(f"{line_index + 1}.0", f"{line_index + 1}.end")

        # Remove all tags from the current line
        for tag in CPU_code_textbox.tag_names():
            CPU_code_textbox.tag_remove(tag, f"{line_index + 1}.0", f"{line_index + 1}.end")
        
        # Update the current line
        syntax_line(line, line_index)
    
    # Restore the selection and cursor
    if selection_start and selection_end:
        CPU_code_textbox.tag_add("sel", selection_start, selection_end)
    CPU_code_textbox.mark_set("insert", cursor_pos)

# update_memory(type) is called to update the memory in the memory tab once registers, ram or call stack have been updated
# If type is true, updates all tabs
def update_memory(update_type="all"):
    # If the current tab isn't the memory tab, return
    if current_tab != "CPU_memory":
        return
    
    # Otherwise, delete all widgets except for the labels
    for widget in registers_frame.winfo_children():
        widget.destroy()
    for widget in ram_frame.winfo_children():
        widget.destroy()
    for widget in call_stack_frame.winfo_children():
        widget.destroy()
    
    # Create register labels
    if update_type == "register" or update_type == "all":
        for register_idx in registers:
            register_label = tk.Label(registers_frame, text=f"{register_idx}: {registers[register_idx]}", bg=dark_gray, fg=white, font=consolas, anchor="w")
            register_label.pack(side="top", fill="x")
    
    # Create ram labels
    if update_type == "ram" or update_type == "all":
        for ram_idx in ram:
            ram_label = tk.Label(ram_frame, text=f"{ram_idx}: {ram[ram_idx]}", bg=light_gray, fg=white, font=consolas, anchor="w")
            ram_label.pack(side="top", fill="x")
    
    # Create register labels
    if update_type == "call_stack" or update_type == "all":
        for call_stack_idx in range(len(call_stack)):
            call_stack_label = tk.Label(call_stack_frame, text=f"{call_stack[call_stack_idx]}", bg=dark_gray, fg=white, font=consolas, anchor="w")
            call_stack_label.pack(side="top", fill="x")

# save_code() is called to save the current code in the textbox
def save_code(save_type=None):
    # Global variables
    global save_file

    # If it's not the code tab, return
    if current_tab != "CPU_code":
        return

    # If save_type doesn't have a value or it has a value and the save_file is empty, open the file explorer
    if not save_type or (save_type and not save_file): 
        ask_file_path = filedialog.asksaveasfilename(
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        # If ask_file_path exists, set save_file to the ask_file_path
        if ask_file_path:
            save_file = ask_file_path
            # If the file doesn't have the .txt extension
            if ask_file_path[len(ask_file_path) - 4:] != ".txt":
                save_file += ".txt" # Add extension
        
        # Otherwise return
        else:
            return
    
    # Set the window title to the file
    window.title(f"CiS Emulator - {save_file}")
    # Save the text in the textbox into the file path given
    with open(save_file, "w") as file:
        file.write(CPU_code_textbox.get("1.0", "end"))

# import_code() is called to import code from a file
def import_code():
    # If it's not the code tab, return
    if current_tab != "CPU_code":
        return
    
    ask_file_path = filedialog.askopenfilename(
        title="Import Code",
        initialdir="/",
        filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
    )

    # If it exists replace the textbox with the code and set save_file to the file path
    if ask_file_path:
        save_file = ask_file_path
        # If the file doesn't have the .txt extension
        if ask_file_path[len(ask_file_path) - 4:] != ".txt":
            save_file += ".txt" # Add extension
        
    # Otherwise return
    else:
        return
    
    # Set the window title to the file
    window.title(f"CiS Emulator - {save_file}")
    # Set the textbox to the things in the file
    with open(save_file, "r") as file:
       CPU_code_textbox.delete("1.0", "end")
       CPU_code_textbox.insert("1.0", file.read())
       syntax_highlighting(True)


#========== Main functions ==========#
update_tabs_on_screen(current_tab)
window.mainloop()