# Example filename: deepgram_test.py
from deepgram import Deepgram
import asyncio
#import json
#import copy
#from itertools import zip_longest
import sys
#from config import *

# Mimetype for the file you want to transcribe
# Include this line only if transcribing a local file
# Example: audio/wav
MIMETYPE = "audio/wav"
API_KEY = '426ede75de63902dcec1758f2825fdecf4144b73'

async def transcribe(lang1,lang2, file):

    # Initialize the Deepgram SDK
    deepgram = Deepgram(API_KEY)
    
    FILE = file
    # Check whether requested file is local or remote, and prepare source
    if FILE.startswith('audio/'):
        audio = open(FILE, 'rb')
        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }
    elif FILE.startswith('http'):
    # file is remote
    # Set the source
        source = {
            'url': FILE
        }
    else:
    # file is local
     # Open the audio file
    #audio = open(FILE, 'rb')

    # Set the source
    #source = {
    #    'buffer': audio,
    #    'mimetype': MIMETYPE
    #}
    
    #audio = open(FILE, 'rb')
        audio = FILE.read()
        source = {
            'buffer': audio,
            'mimetype': MIMETYPE
        }
    # Send the audio to Deepgram and get the response
    if lang1 == 'ko':
        response = await asyncio.create_task(
        deepgram.transcription.prerecorded(
            source,
            {
                'punctuate': True,
                'model' : 'general',
                'tier': 'enhanced',
                'version': 'beta',
                'language': lang1
            }
        )
    )
    else:
        response = await asyncio.create_task(
            deepgram.transcription.prerecorded(
                source,
                {
                    'punctuate': True,
                    'language': lang1
                }
            )
        )
    #print(json.dumps(response))
    words = response['results']['channels'][0]["alternatives"][0]['words']
    for word in words:
        print(word)
    print('---------------')
    # Write the response to the console
    #print(json.dumps(response, indent=4))
    if lang1 == 'zh':
        words = clean_chinese(words)
    if lang1 != lang2:
        if FILE.startswith('audio/'):
            audio = open(FILE, 'rb')
            source = {
                'buffer': audio,
                'mimetype': MIMETYPE
            }
        elif FILE.startswith('http'):
            
            # file is remote
            # Set the source
            source = {
                'url': FILE
            }
        else:
            source = {
                   'buffer': audio,
                    'mimetype': MIMETYPE
            }
        
        #if lang2 == 'ko':
        #    response2 = await asyncio.create_task(
        #        deepgram.transcription.prerecorded(
        #            source,
        #            {
        #                'punctuate': True,
        #                'model' : 'general',
         #               'tier': 'enhanced',
         #               'version': 'beta',
        #                'language': lang2
         #           }
        #        )
        #    )
        #else:
        response2 = await asyncio.create_task(
            deepgram.transcription.prerecorded(
                source,
                {
                    'punctuate': True,
                    'language': lang2
                }
            )
        )
        words2 = response2['results']['channels'][0]["alternatives"][0]['words']
        for word in words2:
            print(word)
        # Write the response to the console
        #print(json.dumps(response2, indent=4))
        # Write only the transcript to the console
        # print(response["results"]["channels"][0]["alternatives"][0]["transcript"])
        if lang2 == 'zh':
            words2 = clean_chinese(words2)
        combined = []
        languages = []
        
        secondIndex = 0
        
        for word in words:

            while secondIndex < len(words2) and word['start'] >= words2[secondIndex]['start']:
                
                combined.append(words2[secondIndex])
                languages.append(lang2)
                secondIndex += 1
            combined.append(word)
            languages.append(lang1)
        
        if secondIndex < len(words2):
            for i in range(secondIndex, len(words2)):
                combined.append(words2[i])
                languages.append(lang2)
        
        cleaned = []
        i = 0
        while i < len(combined)-1:
            
            #edit the logic of this
            if combined[i+1]['start'] - combined[i]['start'] < .1 and languages[i] != languages[i+1]:
                if combined[i+1]['confidence'] > combined[i]['confidence']:
                    cleaned.append(combined[i+1]['punctuated_word'])
                else:
                    cleaned.append(combined[i]['punctuated_word'])
                i = i+1
            else:
                cleaned.append(combined[i]['punctuated_word'])
            i=i+1
        if i < len(combined):
            cleaned.append(combined[i]['punctuated_word'])
    else:
        cleaned = []
        for word in words:
            cleaned.append(word['punctuated_word'])
        
    toRet = " ".join(cleaned)
        
    return toRet

def clean_chinese(words):
    toRet = []
    
    for word in words:
        if len(word['word']) == 1 and ord(word['word']) <= 122:
             continue
        else:
            toRet.append(word)
    return toRet

if __name__ == "__main__":
    try:
        # If running in a Jupyter notebook, Jupyter is already running an event loop, so run transcribe with this line instead:
        # await transcribe()
        
        n = len(sys.argv)-1
        print("number of languages:",n)
        
        if n > 3:
            raise Exception("too many languages.")
        
        print("comfort lang:", sys.argv[1])
        if n > 2:
            
            print("learning lang:", sys.argv[2])
        
        print(asyncio.run(transcribe(sys.argv[1],sys.argv[2],sys.argv[3])))
    except Exception as e:
        exception_type, exception_object, exception_traceback = sys.exc_info()
        line_number = exception_traceback.tb_lineno
        print(f'line {line_number}: {exception_type} - {e}')
