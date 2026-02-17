import main

import unittest as test
from pathlib import Path

asm = main.AsmApi()
fpath = Path(__file__).parent / "test/sort.txt"

print(asm.asm_file(fpath))