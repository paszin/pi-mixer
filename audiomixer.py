import sounddevice

devices = sounddevice.query_devices()

for device in devices:
    if device["name"].startswith("MixVibes U-MIX44"):
        break

print(device)
"""Pass input directly to output.

See https://www.assembla.com/spaces/portaudio/subversion/source/HEAD/portaudio/trunk/test/patest_wire.c

"""
import logging

input_device = device["name"]
output_device = device["name"] # devices[5]["name"] #
samplerate = device["default_samplerate"]
blocksize = 2048
dtype = "int32"
latency = device["default_low_output_latency"]
channels = 4


from functools import partial
import json

class Channel:

    @classmethod
    def init(filename="settings.json"):
        mapping = {0: 0, 1:1, 2:2, 3:3}
        with open("settings.json", "w") as write_file:
            json.dump(mapping, write_file)

    def __init__(self, from_file=False, filename="settings.json"):
        if from_file:
            with open("settings.json", "r") as f:
                self.mapping = json.load(f)
        else:
            self.mapping = {0: 0, 1:1, 2:2, 3:3}
    def get(self, out):
        return self.mapping[out]
    def set(self, out, _in):
        self.mapping[out] = _in
    def getAll(self):
        return self.mapping.values()
    def save(self, filename="settings.json"):
        with open(filename, "w") as write_file:
            json.dump(self.mapping, write_file)



# Channel.init()
masterChannel = Channel()


import sounddevice as sd
import numpy  # Make sure NumPy is loaded before it is used in the callback

def callback(indata, outdata, frames, time, status):
    global masterChannel
    c1, c2, c3, c4 = masterChannel.getAll()
    if status:
        print(status)
    outdata[:] = numpy.array([indata[:,c1], indata[:,c2], indata[:,c3], indata[:,c4]]).T


with sd.Stream(device=(input_device, output_device),
                   samplerate=samplerate, blocksize=blocksize,
                   dtype=dtype, latency=latency,
                   channels=channels, callback=partial(callback)):
    while True:
        print("Select Channel:")
        c = input("channel pair (1 or 2)")
        if c == "1":
            masterChannel.set(0, 0)
            masterChannel.set(1, 1)
            masterChannel.set(2, 0)
            masterChannel.set(3, 1)
            #masterChannel.save()
        elif c == "2":
            masterChannel.set(0, 2)
            masterChannel.set(1, 3)
