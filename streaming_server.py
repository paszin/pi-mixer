from flask import Flask, Response
import sounddevice

import sounddevice

devices = sounddevice.query_devices()
for d in devices:
    pass
    # print(d)

device = {'name': 'HDA Intel PCH: ALC282 Analog (hw:1,0)', 'hostapi': 0, 'max_input_channels': 2, 'max_output_channels': 2, 'default_low_input_latency': 0.005804988662131519, 'default_low_output_latency': 0.005804988662131519, 'default_high_input_latency': 0.034829931972789115, 'default_high_output_latency': 0.034829931972789115, 'default_samplerate': 44100.0}

input_device = device["name"]
output_device = device["name"] # devices[5]["name"] #
samplerate = device["default_samplerate"]
blocksize = 1024
dtype = "int32"
latency = device["default_low_output_latency"]
channels = 1



# def get_wave_fmt_header(samplerate = 44100, channels = 1):
#     data = b'fmt ' # header signature
#     assert len(data) == 4
#     data += bytes([0,0,0,24]) # length
#     assert len(data) == 8
#     data += bytes([0, 1]) # tag
#     assert len(data) == 10
#     data += bytes([0, channels]) # 1 channel
#     assert len(data) == 12
#     data += samplerate.to_bytes(4, 'little')
#     assert len(data) == 16
#     data += samplerate.to_bytes(4, 'little') # abtastrate
#     assert len(data) == 20
#     frame_size = channels * int((samplerate + 7) / 8)
#     data += frame_size.to_bytes(2, 'little')
#     assert len(data) == 22
#     assert len(data) == 24





app = Flask(__name__)


@app.route("/streamfile")
def streammp3():
    def generate():
        with open("sample.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/mpeg")


@app.route("/streamwav")
def streamwav():
    def generate():
        with open("samplepcm.wav", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype='audio/x-wav;version="2 pcm encoding"')


@app.route("/streamwavlive")
def streamwavlive():
    def generate():
        sample_file = open("samplepcm.wav", "rb")
        data = b''
        data += sample_file.read(12)
        fmt_header = sample_file.read(26)
        data += fmt_header
        meta_data = sample_file.read(8)
        length = int.from_bytes(meta_data[4:8], 'little')
        print("len:", length)
        data += meta_data
        data += sample_file.read(length)
        i = 0
        livedata = data[i:i+1024]
        while livedata:
            yield livedata
            i += 1024
            livedata = data[i:i+1024]

    return Response(generate(), mimetype='audio/x-wav;version="2 pcm encoding"')


@app.route("/stream")
def streamlive():
    def generate():
        with sounddevice.InputStream(device=input_device,
                           samplerate=samplerate, blocksize=blocksize,
                           dtype=dtype, latency=latency,
                           channels=channels) as fwav:
            data = fwav.read(1024)
            print(data)
            print(type(data))
            while data:
                #yield bytes(list(data[0]))
                #yield str((list(data[0])))
                yield b''.join(list(data[0]))
                data = fwav.read(1024)
                #print(len(list(data[0])))
    return Response(generate(), mimetype='audio/x-wav;version="1 pcm encoding"') #mimetype="audio/x-wav;codec=pcm")



if __name__ == "__main__":
    app.run(debug=True)
