import os
import json
import requests
import threading
import sox
import wave
import time
import pyaudio

from voice_engine.doa_respeaker_4mic_array import DOA
from datetime import datetime

API_KEY = "<api-key-here>"
API_URI = "<endpoint-here>"

class Mic:
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    RECORD_SECONDS = 3
    DEVICE_ID = "device-0002"
    WAVE_OUTPUT_FILENAME = "output.wav"
    FORMAT = pyaudio.paInt16


    def __init__(self):
        self.thread = threading.Thread(target=self._run)
        self.thread.daemon = True
        self.thread.start()


    def get_audio_data(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT,
                            channels=self.CHANNELS,
                            rate=self.RATE,
                            input=True,
                            frames_per_buffer=self.CHUNK)

        frames = []
        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):
            data = stream.read(self.CHUNK)
            frames.append(data)

        stream.stop_stream()
        stream.close()
        audio.terminate()

        return b''.join(frames), audio.get_sample_size(self.FORMAT)


    def get_audio_stats(self, data, sample_size):
        wf = wave.open(self.WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(sample_size)
        wf.setframerate(self.RATE)
        wf.writeframes(data)
        wf.close()

        recording_data_dict = sox.file_info.stat(self.WAVE_OUTPUT_FILENAME)
        recording_data = list(recording_data_dict.values())
        recording_date = datetime.now()

        doa = DOA(rate=self.RATE)
        doa.put(data)

        return {
            "MinimumAmplitude": str(recording_data[0]),
            "RoughFrequency": str(recording_data[1]),
            "ScaledBy": str(recording_data[2]),
            "MeanNorm": str(recording_data[3]),
            "MaximumDelta": str(recording_data[4]),
            "RmsAmplitude": str(recording_data[5]),
            "Length": str(recording_data[6]),
            "SamplesRead": str(recording_data[7]),
            "VolumeAdjustment": str(recording_data[8]),
            "MinimumDelta": str(recording_data[9]),
            "MidlineAmplitude": str(recording_data[10]),
            "RmsDelta": str(recording_data[11]),
            "MeanAmplitude": str(recording_data[12]),
            "MeanDelta": str(recording_data[13]),
            "MaximumAmplitude": str(recording_data[14]),
            "DeviceId": self.DEVICE_ID,
            "Direction": doa.get_direction(),
            "RecordingDate": recording_date.strftime("%Y%m%d%H%M%S")
        }


    def push_stats(self, stats):
        print("{}".format(stats))
        # requests.post(API_URI, data=json.dumps(stats),
        #     headers={"Content-type": "application/json", "x-api-key": API_KEY})


    def clean(self):
        os.remove(self.WAVE_OUTPUT_FILENAME)


    def _run(self):
        while True:
            data, sample_size = self.get_audio_data()
            stats = self.get_audio_stats(data, sample_size)
            self.push_stats(stats)


start_record = Mic()

if __name__ == '__main__':
    keep_running = True
    while keep_running:
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            keep_running = False
            start_record.clean()
