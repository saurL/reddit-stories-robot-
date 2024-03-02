import pyaudio
import wave
import threading


class AudioRecorder():

    def __init__(self, ):
        self.chunk = 1024  # Record in chunks of 1024 samples
        self.sample_format = pyaudio.paInt16  # 16 bits per sample
        self.channels = 2
        self.fs = 48000  # Record at 44100 samples per second
        self.pyaudio = pyaudio.PyAudio()  # Create an interface to PortAudio
        self.is_recording = False
        self.frames = []
        self.record = threading.Thread(target=self.recording)

    def start_recording(self):
        self.is_recording = True

        self.record.start()

        return

    def stop_recording(self):
        self.is_recording = False

    def save(self, filename):
        # Save the recorded data as a WAV file
        wf = wave.open(filename, 'wb')
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.pyaudio.get_sample_size(self.sample_format))
        wf.setframerate(self.fs)
        wf.writeframes(b''.join(self.frames))
        wf.close()
        self.frames = []

    def recording(self):

        stream = self.pyaudio.open(format=self.sample_format,
                                   channels=self.channels,
                                   rate=self.fs,
                                   frames_per_buffer=self.chunk,
                                   input=True)

        self.frames = []  # Initialize array to store frames

        # w
        while self.is_recording:
            data = stream.read(self.chunk)
            self.frames.append(data)

        # Stop and close the stream
        stream.stop_stream()
        stream.close()
        # Terminate the PortAudio interface
        self.pyaudio.terminate()
