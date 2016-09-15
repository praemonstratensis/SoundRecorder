import gombmatrix-lib as matrix

kb = matrix.keypad_module(0x20,1,1)

while True:
        ch = kb.getch()
        print ch

        if ch == "#":
                exit()