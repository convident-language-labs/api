from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from deepgram_test import transcribe
from pringles import pringles
from chatpgt import call
from googletts import save_audio
from io import BytesIO

import asyncio

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Test!"

@app.route('/stt/<string:lang1>/<string:lang2>/', methods=['POST']) #record audio and transcribe w/ deepgram
def get_transcription(lang1,lang2):
    print("transcribing")
    print(lang1, " ", lang2)

    files = request.files

    file = files.get('file')
    if file is None:
        return jsonify({"transcription": "  "})
    transcription = asyncio.run(transcribe(lang1,lang2,file))
    #transcription = asyncio.run(transcribe(lang1,lang2,fname))
    print(transcription)
    return jsonify({"transcription": transcription})

@app.route('/sttmobile/<string:lang1>/<string:lang2>/', methods=['POST']) #record audio and transcribe w/ deepgram
def get_transcription_mobile(lang1,lang2):
    print("transcribing")
    print(lang1, " ", lang2)
    fileUrl = request.form['fileUrl']
    print(fileUrl)
    if fileUrl is None:
        return jsonify({"transcription": "  "})
    
    transcription = asyncio.run(transcribe(lang1,lang2,fileUrl))
    print(transcription)
    return jsonify({"transcription": transcription})

@app.route('/reply/', methods=['POST']) #chatgpt + pringles
def get_reply():
    if request.method == 'POST':
        text = request.form.get("message")
        replies = call(text)
        try:
            index = int(pringles(replies,text))
        except ValueError:
            index = 1
            
        best = replies[index-1]
        return jsonify({"reply": best}) 
    
@app.route('/speak/<string:targLang>/', methods=["POST"])
def speak_sentence(targLang):
    if request.method == 'POST':
        text = request.form.get("text")
        print(text)
        bytes = save_audio(text,targLang)
        return send_file(bytes,download_name='recording.wav',mimetype="audio/wav")
        #save_audio(text)
        #return jsonify({"response" : "processed"})