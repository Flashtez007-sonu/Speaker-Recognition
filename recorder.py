import sounddevice as sd
from scipy.io.wavfile import write

fs = 44100  # Sample rate
print('recoding')

seconds = 10  # Duration of recording
myrecording = sd.rec(int(seconds * fs), samplerate=fs, channels=2)
sd.wait()  # Wait until recording is finished
sd.stop()
print('Finished Recoding')
write('manish1.wav', fs, myrecording)  # Save as WAV file 
