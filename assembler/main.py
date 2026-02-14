import argparse
from pathlib import Path

class AsmApi:
    def __init__(self):
        pass
    
    def asm_file(self, path: Path):
        with open(path, "r") as f:
            lines = f.readlines()
            return asm(lines)
    
    """Assembles program from lines, then it should return a dict with 0b00000001: [0, 0, 0, ...], but it returns list for now"""
    def asm_string(self, progLines: list) -> dict:
        return asm(progLines)

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
                output = resolveImmediate(operands[0]) + [0, 0, 0] #TODO: replace with resolveLabel
            case "RET": #13
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            case "BRH": #14
                if not operands[1] in flags:
                    print(f"E: Syntax error, invalid flag {operands[1]}")
                    raise SystemExit(1)
                output = resolveImmediate(operands[0]) + flags[operands[1]] #TODO: replace with resolveLabel
            case "RNG": #15
                output = [0, 0, 0, 0, 0, 0, 0, 0] + registers[operands[0]]

            case "JMP": #Pseudo instruction: BRH true
                output = resolveImmediate(operands[0]) + flags["true"] #TODO: replace with resolveLabel
            case "NOP":
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            case "HLT": #0
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

    output.extend(opcode)

    if len(output) != 15:
        print("E: Internal error, output len isn't 15")
        print(f"E: {output}")
        raise SystemExit(1)
    
    print("".join(str(bit) for bit in output))
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

def resolveLabel(value: str) -> list:
    pass

def main():
    parser = argparse.ArgumentParser(
    prog="cis-asm",
    description="CPU in Surival - Assembler"
    )
    parser.add_argument("input_file")
    parser.add_argument("--out", help="Output file")

    args = parser.parse_args()

    if not Path(args.input_file).exists():
        print("E: The input file doesn't exist")
        raise SystemExit(1)
    
    with open(args.input_file, "r") as f:
        lines = f.readlines()
        asm(lines)

def asm(lines):
    output = []
    for line in lines:
        if ";" in line.strip():
            line = line.split(";")[0].strip()
            if not line:
                continue
        
        if line.strip().startswith("@"):
            continue        
        if line.strip().startswith("."):
            continue
        
        if line.strip() == "":
            continue

        # Normal instruction    
        i = line.replace("\n", "").split(" ")
        output.extend(makeInstruction(i[0].upper(), i[1:]))

    print(".")
    return output

if __name__ == "__main__":
    main()