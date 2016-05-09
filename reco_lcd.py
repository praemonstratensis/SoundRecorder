import pyaudio
import wave
import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

inpin = 4

gpio.setup(inpin, gpio.IN)

# CHUNK = 256
CHUNK = 8192
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 15

if int(time.strftime("%H")) <= 8 and int(time.strftime("%U")) == 02:
	WAVE_OUTPUT_FILENAME = "./records/Elmelkedes_" + (str(time.strftime("%H:%M-%d_%m_%y" )) + ".wav")
else:
	WAVE_OUTPUT_FILENAME = "./records/REC_" + (str(time.strftime("%H:%M-%d_%m_%y" )) + ".wav")

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print("* recording")

frames = []

#for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
while gpio.input(inpin) == 0:
    data = stream.read(CHUNK)
    frames.append(data)

print("* done recording")

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()
