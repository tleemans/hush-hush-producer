import pyaudio
import wave
import sox
import requests
import json

from datetime import datetime

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "output.wav"

headers = {
    'Content-type': 'application/json',
    'x-api-key': '<api-key-here>' 
}

print ("+---------------------------------+")
print ("| Press Ctrl+C to Break Recording |")
print ("+---------------------------------+")

global keep_going
keep_going = True

while keep_going:
    try:
        audio = pyaudio.PyAudio()

        stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

        print("* recording")
        frames = []
        for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
            data = stream.read(CHUNK)
            frames.append(data)
        print("* done recording")

        stream.stop_stream()
        stream.close()
        audio.terminate()

        wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()

        recording_data_dict = sox.file_info.stat(WAVE_OUTPUT_FILENAME)
        recording_data = list(recording_data_dict.values())
        recording_date = datetime.now()

        data = {}
        data['DeviceId'] = "device-0002"
        data["RecordingDate"] = recording_date.strftime("%Y%m%d%H%M%S")
        data["MinimumAmplitude"] = str(recording_data[0])
        data["RoughFrequency"] = str(recording_data[1])
        data["ScaledBy"] = str(recording_data[2])
        data["MeanNorm"] = str(recording_data[3])
        data["MaximumDelta"] = str(recording_data[4])
        data["RmsAmplitude"] = str(recording_data[5])
        data["Length"] = str(recording_data[6])
        data["SamplesRead"] = str(recording_data[7])
        data["VolumeAdjustment"] = str(recording_data[8])
        data["MinimumDelta"] = str(recording_data[9])
        data["MidlineAmplitude"] = str(recording_data[10])
        data["RmsDelta"] = str(recording_data[11])
        data["MeanAmplitude"] = str(recording_data[12])
        data["MeanDelta"] = str(recording_data[13])
        data["MaximumAmplitude"] = str(recording_data[14])

        r = requests.post("<endpoint-here>", data=json.dumps(data), headers=headers)
    except KeyboardInterrupt:
        keep_going=False
    except:
        pass
