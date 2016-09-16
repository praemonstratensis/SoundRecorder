#gspread git: https://github.com/burnash/gspread

import gspread
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds']

credentials = ServiceAccountCredentials.from_json_keyfile_name('pi-spreadsheet-143506.json', scope)

gc = gspread.authorize(credentials)

leltar = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ors3F0nnfuUeGzuvleBAHNBZSD5sG5BuiRBoRnLL78s/edit#gid=0')

hangtech = leltar.get_worksheet(1)

a2 = hangtech.acell('A2').value

print a2

hangtech.update_acell('M2', 'haliho')