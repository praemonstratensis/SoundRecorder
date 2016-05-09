import RPi.GPIO as gpio 
import time 
import os 
import outlook
import Adafruit_CharLCD as LCD
from datetime import datetime

#LCD kezeleshez az lcd definialasa
lcd = LCD.Adafruit_CharLCDPlate()

#a levelkezelo elinditasa (https://github.com/awangga/outlook)
mail = outlook.Outlook()

#gpio beallitasa
gpio.setmode(gpio.BCM)

buzzPin = 27
trigPin = 4
tru = 1
wasBuzz = 0
commandPin = 22

gpio.setup(trigPin, gpio.IN)

gpio.setup(buzzPin, gpio.OUT)
gpio.output(buzzPin, 0)

gpio.setup(commandPin, gpio.OUT) 
gpio.output(commandPin, 0)

def new_log(on, off):
	#logolas, amely minden nap egy fajlt hoz letre, es abba irogatja a napi bekapcsolasokat/kikapcsolasokat HH:MM formatumban
	#meg kell adni neki a hangositas bekapcsolasanak(on) es kikapcsolasanak(off) idopontjat (altalanos idoformatumban ajanlott(time.time() fuggvennyel lehet lekerni))
	try: 
		#ha mar letezik aznapi fajl, akkor abba iras
		log = open("./log/LOG_" + str(time.strftime("%d-%m-%Y")) + ".txt", "a")
	except: 
		#na nem letezik, akkor uj letrehozasa
		log = open("./log/LOG_" + str(time.strftime("%d-%m-%Y")) + ".txt", "w")
	ontime = time.strftime("%H:%M", time.localtime(on))
	offtime = time.strftime("%H:%M", time.localtime(off))
	text = "\nBE: " + str(ontime) + " KI: " + str(offtime)
	log.write(text)
	log.close()

def checkmail():
	#Email fiok ellenorzo automata
	mail.login('premirpi@outlook.com','Premi123')
	mail.inbox()
        level = mail.unread()
   	levelstr = str(level)

        return levelstr;

def sendmail(to,message):
	#levelkuldo automata, mely a level targyanak automatikusan a feljebb olvashato szoveget allitja be
	#a fuggvenynek meg kell adni a cimzettet, illetve a level tartalmat
        mail.sendEmail(to,'Automatikusan a Studiobol kuldott uzenet',message)

def buzz():
	#csipogas(Ez a funkcio jelenleg nem mukodik, ugyanis meghibasodott a buzzer)
	gpio.output(buzzPin, 1)
	time.sleep(0.5)
	gpio.output(buzzPin, 0)

def log():
	#logolas(regi verzio, mar nem hasznalom)
	tim = time.asctime( time.localtime(time.time()) )
	log = open('log.txt','a')
	log.write(tim + '\n')
	log.close()

def upload(filename, type):
	#fajl feltoltese, utmutato: http://raspi.tv/2013/how-to-use-dropbox-with-raspberry-pi
	#a fuggvenynek meg kell adni a feltoltendo fajl nevet, illetve, hogy az Log, vagy Felvetel-e(log/felvetel)
	#if type == "log":
	#	os.system("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/log/" + filename + " /log/" + filename)
	#elif type == "rec":
	#	os.system("/home/pi/Dropbox-Uploader/dropbox_uploader.sh upload /home/pi/rec/" + filename + " Felvett_bemondasok/" + filename)

last_check = time.time()
wasLogUpload = 0


while tru == 1:
	if time.strftime("%H:%M:%S") == "6:00:00":
		#reggel 6 orakor a "logfajl feltoltese mar megtortent" valtozot visszaallitjuk 
		wasLogUpload = 0	

	if gpio.input(trigPin) == 0 and wasBuzz == 0:
		#bekapcsolt allapot
		#buzz() #csipogas
		on_time = time.time()
		#log() #logolas
		wasBuzz = 1
		print "A hangositas bekapcsolt.\n"

                #lcdre kiirni, hogy bekapcsolt
                lcd.clear()
                lcd.message("A hangositas\n      bekapcsolt")

		#hangfelvetel elinditasa es leallitasa, ha kikapcsol a hangositas
		if int(time.strftime("%H")) <= 8 and int(time.strftime("%U")) == 02:
			#amennyiben hetfo reggel 8 ora elott keszul a felvetel Elmelkedes... neven mentjuk el
	        	WAVE_OUTPUT_FILENAME = "./rec/Elmelkedes_" + (str(time.strftime("%H:%M-%d_%m_%y" )) + ".wav")
		else:
			#ha nem, akkor REC... neven
		        WAVE_OUTPUT_FILENAME = "./rec/REC_" + (str(time.strftime("%H:%M-%d_%m_%y" )) + ".wav")
		os.system("sudo python ./rec/reco_lcd.py &")
		
	elif gpio.input(trigPin) == 1 and wasBuzz == 1:
		#Kikapcsolt allapot
		off_time = time.time()
		
		#logolas
		new_log(on_time, off_time)
		
		wasBuzz = 0
		print "A hangositas kikapcsolt.\n"
		
		#lcdre kiirni, hogy kikapcsolt
		lcd.clear()
                lcd.message("A hangositas\n      kikapcsolt")
	
		#felvetel feltoltese Dropboxra ha hetfo reggeli elmelkedes volt
		if int(time.strftime("%H")) <= 8 and int(time.strftime("%U")) == 02:
			upload(filename, "rec")

		#email kuldese, a hangositasi informaciokkal(idegesito, mert naponta 5-6 emailt kuld, ezert nincs aktivalva, helyette van az uj logfajl elkuldo, amely naponta csak este 7kor tolti fel Dropboxra az aznapi bekapcsolasokat)
		#mail.login('premirpi@outlook.com','Premi123')
                #sendmail("premontrei.studio@gmail.com", " Hang felveve es mentve " + filename + " neven. Tovabbi szep napot!")

		#lcd torlese
                time.sleep(4)
                lcd.clear()
		lcd.message("Nyomd meg a kiv.\ngombot a menuhoz!")

	if  time.time()-last_check>20:
		print "Leveltar ellenorzese"
		try:
			level = checkmail()
			print "A lehet, hogy nem letezo level tartalma: "#+level
		except:
			level = "nothing"
			print "nincs level"
		last_check = time.time()
		 
		if level == "nothing":
			print "Email ellenorizve, semmi nem volt"
		elif level != "nothing":
			#level targyanak, azaz a parancsnak a kiszedese
			sec_part = level.split("Subject: ")[1]
        		subjectn = sec_part.split("From:")[0]
	        	command = subjectn.split("\n")[0]
			
			#level kuldojenek kiszedese
			sec_part = level.split("From: ")[1]
                	sendern = sec_part.split("<")[1]
               	 	sender = sendern.split(">")[0]
		
			#level testenek kiszedese (igen kiforratlan funkcio)
			resz1 = level.split('Content-Type: ')[3]
			resz2 = resz1.split('\n')[1]
			body = resz2.split('\n')[0]

			print "command: " + command
			print "sender: " + sender
			print "body: " + body

			if command == "play":
				print "play"
				sendmail(sender,"Zene elinditva. \n Udv, PremiRPi")
				os.system("sudo mpg321 -q asd.mp3 &")
			elif command == "sendmemail":
				print "sendmemail" 
				sendmail(sender,"Kuldtel magadnak egy uzenetet! :-) \n Udv, PremiRPi \n A te leveled ez volt: " + body)
		
			#elif command == "":
			#	print "kex"
			#	sendmail(sender,"Nincs ilyen parancs! :-( \n Udv, PremiRPi")	
		
		print "\n"
	
	#innentol lefele a menu vezerlese van, amely egy igen kiforratlan funkcio
	if int(time.strftime("%H")) == 7 and wasLogUpload == 0:
		filename = "/LOG_" + str(time.strftime("%d-%m-%Y")) + ".txt"
		upload(filename, "log")
		wasLogUpload = 1

	if lcd.is_pressed(LCD.SELECT):
		lcd.clear()
		lcd.message("MENU")

		m = 0
		
	if lcd.is_pressed(LCD.DOWN):
		m = m-1
	if lcd.is_pressed(LCD.UP):
		m = m+1
	if lcd.is_pressed(LCD.LEFT):
		lcd.clear()
		lcd.message("Kilepes a \n      menubol...")
				
	
	#elif gpio.input(commandPin):
		#command = raw_input()
		#ide olyan parancsok kerulhetnek, amiket vergehajthat a pi, pl.: bekapcsolas, suliradio, stb.
	
	time.sleep(0.1)
gpio.cleanup()
