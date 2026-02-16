import argparse
from pathlib import Path

labels = {}
progCounter = -1  # Magic number
labelCounter =  0 # Magic number
# Counts Lines in File
LineCounter = 0

class AsmApi:
    def __init__(self):
        pass
    
    def asm_file(self, path: Path):
        with open(path, "r") as f:
            lines = f.readlines()
            return asm(lines)
    
    """Assembles program from lines, then it should return a dict with 0b00000001: [0, 0, 0, ...]"""
    def asm_string(self, progLines: list) -> dict:
        return asm(progLines)

def binPad(string, lenght=8):
    return string.zfill(lenght)

def makeInstruction(name: str, operands: list) -> list:
    output = []

    opcodes = {
        "HLT": [ 0, 0, 0, 0 ],
        "NOT": [ 0, 0, 0, 1 ],
        "ADD": [ 0, 0, 1, 0 ],
        "SUB": [ 0, 0, 1, 1 ],
        "AND": [ 0, 1, 0, 0 ],
        "XOR": [ 0, 1, 0, 1 ],
        "NOR": [ 0, 1, 1, 0 ],
        "RSH": [ 0, 1, 1, 1 ],
        "LDI": [ 1, 0, 0, 0 ],
        "ADI": [ 1, 0, 0, 1 ],
        "CAL": [ 1, 1, 0, 0 ],
        "RET": [ 1, 1, 0, 1 ],
        "BRH": [ 1, 1, 1, 0 ],
        "RNG": [ 1, 1, 1, 1 ],

        "LOD": [ 1, 0, 1, 0 ],
        "STO": [ 1, 0, 1, 0 ],
        "REQ": [ 1, 0, 1, 1 ],
        "OUT": [ 1, 0, 1, 1 ],

        "JMP": [ 1, 1, 1, 0 ]
    }

    registers = {
        "0":  [ 0, 0, 0],
        "r0": [ 0, 0, 0],
        "r1": [ 0, 0, 1],
        "r2": [ 0, 1, 0],
        "r3": [ 0, 1, 1],
        "r4": [ 1, 0, 0],
        "r5": [ 1, 0, 1],
        "r6": [ 1, 1, 0],
        "r7": [ 1, 1, 1],
    }

    flags = {
        "true":  [ 0, 0, 0],
        "msb":   [ 0, 0, 1],
        "zero":  [ 0, 1, 0],
        "cout":  [ 0, 1, 1],
        "lsb":   [ 1, 0, 0],
        "!msb":  [ 1, 0, 1],
        "!zero": [ 1, 1, 0],
        "!cout": [ 1, 1, 1]
    }

    opcode = opcodes[name]
    
    match name:
            case "NOT": #1
                output = [ 0, 0, 0, 0, 0] + registers[operands[1]] + registers[operands[0]]
            case "ADD": #2
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
            case "SUB": #3
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
            case "AND": #4
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
            case "XOR": #5
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
            case "NOR": #6
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
            case "RSH": #7
                output = [ 0, 0, 0, 0, 0] + registers[operands[1]] + registers[operands[0]]
            case "LDI": #8
                output = resolveImmediate(operands[1]) + registers[operands[0]]
            case "ADI": #9
                output = resolveImmediate(operands[1]) + registers[operands[0]]
            case "LOD": #10
                print("")
            case "STR": #10
                print("")
            case "REQ": #11
                print("")
            case "OUT": #11
                print("")
            case "CAL": #12
                output = resolveLabel(operands[0]) + [0, 0, 0]
            case "RET": #13
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            case "BRH": #14
                if not operands[1] in flags:
                    print(f"E: Syntax error, invalid flag {operands[1]}")
                    raise SystemExit(1)
                output = resolveLabel(operands[0]) + flags[operands[1]]
            case "RNG": #15
                output = [0, 0, 0, 0, 0, 0, 0, 0] + registers[operands[0]]

            case "JMP": #Pseudo instruction: BRH true
                output = resolveLabel(operands[0]) + flags["true"]
            case "NOP":
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            case "HLT": #0
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    output.extend(opcode)

    if len(output) != 15:
        # ANSI Color codes
        red = "\033[31m"
        cyan = "\033[36m"
        rst = "\033[0m" # Reset
        print(f"{red}E:{rst} Expected {cyan}15{rst} bits got {cyan}{len(output)}{rst} bits")
        print(f"    Line: {cyan}{LineCounter}{rst}, Instruction {cyan}{name} {operands}{rst}")
        print(f"    Binary Instruction: {cyan}{output}{rst}")
        exit(1)
    return output

def resolveImmediate(value: str) -> list:
    out = []
    if value.startswith("0d"):
        out = bin(int(value.replace("0d", ""), 10)).replace("0b", "")
    elif value.startswith("0x"):
        out = bin(int(value.replace("0x", ""), 16)).replace("0b", "")
    elif value.startswith("0b"):
        out = value.replace("0b", "")
    else:
        pass
    
    return list(out)

def counter(increase: int):
    global progCounter

    if increase:
        progCounter += 1
    
    return "b" + binPad(bin(progCounter).replace("0b", ""))

def counterLabel(increase: int):
    global labelCounter

    if increase:
        labelCounter += 1
    
    return "b" + binPad(bin(labelCounter).replace("0b", ""))

def resolveLabel(value: str) -> list:
    if ( value.startswith("0x") or value.startswith("0d") or value.startswith("0b") ):
        return resolveImmediate(value)
    
    if value.startswith("."):
        value = value.removeprefix(".").replace("\n", "")

    if not value in labels:
        print("E: Syntax error, undefined label") #TODO: resolve labels at end of execution
        print(f"E: {value}")
        exit(1)

    return list(labels[value].replace("b", ""))

def main():
    parser = argparse.ArgumentParser(
        prog="cis-asm",
        description="CPU in Surival - Assembler"
    )
    parser.add_argument("input_file")
    parser.add_argument("--out", help="Output file")
    parser.add_argument("--print-ops", help="Print full instruction input")
    args = parser.parse_args()

    if not Path(args.input_file).exists():
        print("E: The input file doesn't exist")
        exit(1)
    
    with open(args.input_file, "r") as f:
        lines = f.readlines()
        asm(lines, bool(args.print_ops))

def asm(lines: list[str], printOps: bool):
    output = {}
    linesP = []

    macros = {}

    # Preprocessor
    for line in lines:
        if ";" in line.strip():
            line = line.split(";")[0].strip()
            if not line:
                continue
        
        if line.strip().startswith("@"):
            macro = line.strip().removeprefix("@").replace("\n", "").split(" ")

            if macro[0] == "def":
                if not (len(macro) - 1) == 2:
                    print("E: Syntax error, invalid @def macro")
                    print(f"E: Expected 2 arguments got {len(macro) - 1}")
                    exit(1)
                macros[macro[1]] = macro[2]
                continue
            elif macro[0] == "inline":
                print("E: Internal error, @inline not implemented")
                exit()
                #continue
            else:
                print("E: Syntax error, invalid macro")
                print(f"E: {line}")
                exit(1)

        if line.strip().startswith("."):
            label = line.strip().removeprefix(".")
            labels[label] = counterLabel(False)
            continue
        
        if line.strip() == "":
            continue
        
        for key, replaceStr in macros.items():
            line = line.replace(key, replaceStr)
        
        linesP.append(line)
        counterLabel(True)

    # Assembler
    for line in linesP:
        # Count Real lines to show where error happened smh smh
        global LineCounter
        LineCounter += 1

        # Normal instruction
        i = line.replace("\n", "").split()
        output[counter(True)] = makeInstruction(i[0].upper(), i[1:])

        d = "".join(str(bit) for bit in output[counter(False)])

        labelsSwaped = {v: k for k, v in labels.items()}
        logLabel = ""
        if counter(False) in labelsSwaped:
            logLabel = labelsSwaped[counter(False)]
        print(counter(False).replace("1", "█").replace("0", " ") + " " + d + " " + (( "".join((str(v) + " ") for v in i) ) if printOps else i[0] ) + " " + logLabel) # If label log it (labels[counter(False)] if counter(False) in labels else "")

    print(".")
    print(labels)
    return output

if __name__ == "__main__":
    main()