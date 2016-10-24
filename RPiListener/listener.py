#gspread git: https://github.com/burnash/gspread
#gombmatrix lib: http://www.mikronauts.com/raspberry-pi/raspberry-pi-i2c-4x4-matrix-keypad-with-mcp23017-and-python/2/

import RPi.GPIO as gpio
import ConfigParser
import sys
import datetime
import time
import shlex, subprocess
import requests
import tty, termios
import os

char = ""
code = ""

config = ConfigParser.ConfigParser()
config.read("/etc/recorder.ini")

def ConfigSectionMap(section):
        dict1 = {}
        options = config.options(section)
        for option in options:
                try:
                        dict1[option] = config.get(section, option)
                        if dict1[option] == -1:
                                DebugPrint("skip: %s" % option)
                except:
                        print("exception on %s!" % option)
                        dict1[option] = None
        return dict1

trigPin = 5

#gpio beallitasa
gpio.setmode(gpio.BCM)
gpio.setup(trigPin, gpio.IN)#, pull_up_down=gpio.PUD_DOWN
upload_url = ConfigSectionMap("uploader")['server_address']
record_everything = ConfigSectionMap("listener")['record_everything'] == 'true'
record_days = map(lambda x: int(x), ConfigSectionMap("listener")['record_days'].split(','))
record_start = datetime.datetime.strptime(ConfigSectionMap("listener")['record_start'], '%H:%M')
record_end = datetime.datetime.strptime(ConfigSectionMap("listener")['record_end'], '%H:%M')
record_in_progress = False

os.system("sudo bash /home/pi/Record_from_lineIn.sh")

while True:
        #felveo resz
        if gpio.input(trigPin) == 0 and not record_in_progress:
                #bekapcsolt allapot
                today = datetime.datetime.today().weekday() + 1
                now = datetime.datetime.now()
                sound_filename = "Elmelkedes_" + time.strftime("%Y_%m_%d_%H_%M_%S") 
                sound_filename_wav = sound_filename + ".wav"
                record_script = shlex.split('arecord -Dhw:sndrpiwsp -c 2 -f s16_LE -r 44100')
                record_script.append(sound_filename_wav)

                print "A hangositas bekapcsolt.\n"
                should_start_rec = record_everything or (today in record_days and record_start.time() <= now.time() and record_end.time() >= now.time())

                if should_start_rec:
                        record_in_progress = True
                        process = subprocess.Popen(record_script)

        elif gpio.input(trigPin) == 1 and record_in_progress:
                #Kikapcsolt allapot

                if record_in_progress:
                        process.terminate()
                        record_in_progress = False

                        sound_filename_mp3 = sound_filename + ".mp3"
                        sound_filename_mp3_tiszta = sound_filename + "_zajszurt.mp3"

                        convert_script = "ffmpeg -i " + sound_filename_wav + " -acodec libmp3lame " + sound_filename_mp3
                        #os.system(convert_script)

                        norm_command = "sox --norm " + sound_filename_wav + " " + sound_filename_mp3
                        os.system(norm_command)

                        noise_command_part1 = "sox "  + sound_filename_mp3 +" -n trim 0 1.5 noiseprof speech.noise-profil"
                        #os.system(noise_command_part1)

                        noise_command_part2 = "sox " + sound_filename_mp3 + " " + sound_filename_mp3_tiszta + " noisered speech.noise-profile 0"
                        #os.system(noise_command_part2)

                        rm_wav_script = "rm " + sound_filename_wav
                        os.system(rm_wav_script)

                        files = {'sound_file': open(sound_filename_mp3, 'rb')}
                        response = requests.post(upload_url, files=files)
                        print response.text

                        #files = {'sound_file': open(sound_filename_mp3_tiszta, 'rb')}
                        #response = requests.post(upload_url, files=files)
                        #print response.text

                print "A hangositas kikapcsolt, hang felveve es feltoltve a szerverre.\n"

        time.sleep(0.1)
gpio.cleanup()
