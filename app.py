from flask import Flask, send_file, Response, request
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
from pydub.effects import speedup

app = Flask(__name__)

@app.errorhandler(404)
def streamogg(e):
    path = request.path
    tts = gTTS(text=path, lang=request.args.get("l", default="en"))
    tts.save("temp.mp3")

    audio = AudioSegment.from_mp3("temp.mp3")
    audio = speedup(audio, playback_speed=float(request.args.get("s", default=1.25)))
    louder_audio = audio + int(request.args.get("v", default=10))
    louder_audio.export("audio.ogg", format="ogg")

    def generate():
        with open("audio.ogg", "rb") as fau:
            data = fau.read(1024)
            while data:
                yield data
                data = fau.read(1024)

    return Response(generate(), mimetype="audio/ogg")

if __name__ == "__main__":
    app.run()
