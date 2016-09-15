from Adafruit_MCP230XX import Adafruit_MCP230XX
import time

mcp = Adafruit_MCP230XX(address = 0x20, num_gpios = 16) # MCP23017

buttons = [ [1,2,3,"A"],
            [4,5,6,"B"],
            [7,8,9,"C"],
            ["*",0,"#","D"] ]

col = [12,13,14,15]
rows = [8,9,10,11]

for i in range(4):
        mcp.config(rows[i], mcp.INPUT)
        mcp.pullup(rows[i], 1)
        mcp.config(col[i], mcp.OUTPUT)

while True:
        for j in range(4):
                mcp.output(col[j], 0)

                i = 0
                for i in range(4):
                        if mcp.input(rows[i]) == 0:
                                print buttons[i][j]
                                while(mcp.input(rows[i]) == 0):
                                        pass
                mcp.output(col[j], 1)
