#gspread git: https://github.com/burnash/gspread
#gombmatrix lib: http://www.mikronauts.com/raspberry-pi/raspberry-pi-i2c-4x4-matrix-keypad-with-mcp23017-and-python/2/

import gspread
from oauth2client.service_account import ServiceAccountCredentials
import gombmatrix_lib as matrix
import time

kb = matrix.keypad_module(0x20,1,1) 

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('pi-spreadsheet-143506.json', scope)

gc = gspread.authorize(credentials)

leltar = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ors3F0nnfuUeGzuvleBAHNBZSD5sG5BuiRBoRnLL78s/edit#gid=0')

fenytech = leltar.get_worksheet(0)
hangtech = leltar.get_worksheet(1)
kabel = leltar.get_worksheet(2)
kolcson = leltar.get_worksheet(3)

char = ""
code = ""

def updateBorrow(row_values, happening):
    if happening == 'back':
        i = 1
        lastIdRow = 0
        #print kolcson.cell(i, 1).value
        while kolcson.cell(i, 1).value != "":
            print kolcson.cell(i, 1).value
            if kolcson.cell(i, 1).value == row_values[0]:
                lastIdRow = i
            i += 1

        kolcson.update_cell(lastIdRow, 4, time.strftime("%Y_%m_%d_%H_%M"))
    else:
        # ha nincs adatbazisban, a legelso ures sorba iras
        free_row = 2
        while kolcson.cell(free_row, 1).value != "":
            free_row = free_row + 1


        kolcson.update_cell(free_row, 1, row_values[0])
        kolcson.update_cell(free_row, 2, row_values[1])
        kolcson.update_cell(free_row, 3, time.strftime("%Y_%m_%d_%H_%M"))

while True:
	char = kb.getch()

	if char == "*":
		code = ""
	elif char == "#":
		if "FT" in code:
			try:
				cell = fenytech.find(code)
				#row = fenytech.row_values(cell.row)
				print time.strftime("%Y_%m_%d_%H_%M")
				print fenytech.cell(cell.row, cell.col+1).value

				agi = fenytech.cell(cell.row, 12).value
				if agi == "":
					fenytech.update_cell(cell.row, 12, 'Nem')
					fenytech.update_cell(cell.row, 13, time.strftime("%Y_%m_%d_%H_%M"))
					fenytech.update_cell(cell.row, 14, '')

					updateBorrow(fenytech.row_values(cell.row), 'out')
					print "ki"
				else:
					fenytech.update_cell(cell.row, 12, '')
					fenytech.update_cell(cell.row, 14, time.strftime("%Y_%m_%d_%H_%M"))

					updateBorrow(fenytech.row_values(cell.row), 'back')
					print "vissza"
			except:
				print "Rossz leltari szam, code reset"
				code = ""
		elif "HE" in code:
			try:
				cell = hangtech.find(code)
				print time.strftime("%Y_%m_%d_%H_%M")
				print hangtech.cell(cell.row, cell.col+1).value

				agi = hangtech.cell(cell.row, 13).value
				if agi == "":
					hangtech.update_cell(cell.row, 13, 'Nem')
					hangtech.update_cell(cell.row, 14, time.strftime("%Y_%m_%d_%H_%M"))
					hangtech.update_cell(cell.row, 15, '')

					updateBorrow(hangtech.row_values(cell.row), 'out')
					print "ki"
				else:
					hangtech.update_cell(cell.row, 13, '')
					hangtech.update_cell(cell.row, 15, time.strftime("%Y_%m_%d_%H_%M"))

					updateBorrow(hangtech.row_values(cell.row), 'back')
					print "vissza"
			except:
				print "Rossz leltari szam, code reset"
				code = ""
			
		elif "K" in code or "A" in code:
			try:
				cell = kabel.find(code)
				print time.strftime("%Y_%m_%d_%H_%M")
				print kabel.cell(cell.row, cell.col+1).value

				agi = kabel.cell(cell.row, 10).value
				if agi == "":
					kabel.update_cell(cell.row, 10, 'Nem')
					kabel.update_cell(cell.row, 11, time.strftime("%Y_%m_%d_%H_%M"))
					kabel.update_cell(cell.row, 12, '')

					updateBorrow(kabel.row_values(cell.row), 'out')
					print "ki"
				else:
					kabel.update_cell(cell.row, 10, '')
					kabel.update_cell(cell.row, 12, time.strftime("%Y_%m_%d_%H_%M"))
					
					updateBorrow(kabel.row_values(cell.row), 'back')
					print "vissza"
			except:
				print "Rossz leltari szam, code reset"
				code = ""
			

		code = ""

	else:
		code += char
		print "Szam: " + code