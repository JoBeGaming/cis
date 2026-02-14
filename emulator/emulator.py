import re
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

    # Colors for syntax highlighting (got this from chatgpt aswell and edited it a bit :3)
    CPU_code_content.tag_configure("opcode", foreground="#569CD6")
    CPU_code_content.tag_configure("register", foreground="#4EC9B0")
    CPU_code_content.tag_configure("ram", foreground="#CE9178")
    CPU_code_content.tag_configure("immediate", foreground="#B5CEA8")
    CPU_code_content.tag_configure("comment", foreground="#6A9955")
    CPU_code_content.tag_configure("label", foreground="#C586C0")
    CPU_code_content.tag_configure("default", foreground="#D4D4D4")
    CPU_code_content.tag_configure("flag", foreground="#EBEB99")

# i used chatgpt for this
def syntax_highlighting():
    # First, clear all existing tags
    #for tag in ["opcode", "register", "immediate", "comment", "label"]:
        #CPU_code_content.tag_remove(tag, "1.0", tk.END)

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
    window.after(100, syntax_highlighting)

syntax_highlighting()
window.mainloop()