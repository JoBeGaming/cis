import argparse
from pathlib import Path

def makeInstruction(name: str, operands: list):
    output = []

    opcodes = {
        "HLT": [ 0, 0, 0, 0 ],
        "NOT": [ 0, 0, 0, 1 ],
        "AND": [ 0, 0, 1, 0 ],
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

    opcode = opcodes[name]
    
    match opcode:
            case "NOT": #1
                print("")

            case "ADD": #2
                output = [ 0, 0] + registers[operands[2]] + registers[operands[1]] + registers[operands[0]]
                output.extend(opcode)
            case "SUB": #3
                #output = [0, 0] + operands[2] + operands[1] + operands[0] + opcode
            case "AND": #4
                
            case "XOR": #5
                
            case "NOR": #6
                
            case "RSH": #7
                print("")
            case "LDI": #8
                print("")
            case "ADI": #9
                print("")
            case "LOD": #10
                print("")
            case "STR": #10
                print("")
            case "REQ": #11
                print("")
            case "OUT": #11
                print("")
            case "CAL": #12
                print("")
            case "RET": #13
                print("")
            case "BRH": #14
                print("")
            case "RNG": #15
                print("")

            case "JMP": #Pseudo instruction: BRH true
                print("")
            case "NOP":
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                output.extend(opcode)
            case "HLT": #0
                output = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]
                output.extend(opcode)

    return output

parser = argparse.ArgumentParser(
    prog="cis-asm",
    description="CPU in Surival - Assembler"
)
parser.add_argument("input_file")
parser.add_argument("--out", help="Output file")

args = parser.parse_args()
output = []

if not Path(args.input_file).exists():
    print("E: The input file doesn't exist")
    raise SystemExit(1)

with open(args.input_file, "r") as f:
    lines = f.readlines() 
    for line in lines:
        if ";" in line.strip():
            pass
        if line.strip().startswith("."):
            break

        # Normal instruction    
        i = line.split(" ")
        
        output.extend(makeInstruction(i[0], ))