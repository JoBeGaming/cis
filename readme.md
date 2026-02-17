# Redstone CPU in Survival Project

Source structure:
```
assembler/ - CiS Assembler and Schem-Generator
emulator/ - CiS Emulator and editor code with syntax highlighting
```

## ISA <!--todo do proper docs for LOD, STR, REQ and OUT-->

| Opcode   | Operand 1 | Operand 2 | Operand 3 | Other |
|:---------|:---------:|:---------:|:---------:|:------:|
| HLT | - | - | - | - |
| RET | - | - | - | - |
| RNG | Reg 1 | - | - | - |
| NOT | Reg 1 | Reg 2 | - | - |
| ADD | Reg 1 | Reg 2 | Reg 3 | - |
| SUB | Reg 1 | Reg 2 | Reg 3 | - |
| AND | Reg 1 | Reg 2 | Reg 3 | - |
| XOR | Reg 1 | Reg 2 | Reg 3 | - |
| NOR | Reg 1 | Reg 2 | Reg 3 | - |
| RSH | Reg 1 | Reg 2 | - | - |
| LDI | Reg 1 | Immediate | - | - |
| ADI | Reg 1 | Immediate | - | - |
| LOD | - | - | - | - | 
| STR | - | - | - | - |
| REQ | - | - | - | - |
| OUT | - | - | - | - |
| CAL | Label | - | - | - |
| BRH | Label | Flags | - | - |
| JMP | Label | - | - | - |