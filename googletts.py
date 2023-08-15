import os
import io
#from pydub import AudioSegment
#from pydub.playback import play

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="key.json"

from google.cloud import texttospeech

def save_audio(text,targLang):
    
    # Instantiates a client
    client = texttospeech.TextToSpeechClient()

    # Set the text input to be synthesized
    synthesis_input = texttospeech.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") 
    # ****** the NAME
    # and the ssml voice gender ("neutral")
    if targLang == 'zh':
        voice = texttospeech.VoiceSelectionParams(
            language_code='cmn-CN',
            name='cmn-CN-Wavenet-C',
            ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    elif targLang == 'ko':
        voice = texttospeech.VoiceSelectionParams(
            language_code='ko-KR',
            name='ko-KR-Neural2-C',
            ssml_gender=texttospeech.SsmlVoiceGender.MALE)
    else:
        voice = texttospeech.VoiceSelectionParams(
            language_code='en-US',
            name='en-US-Neural2-D',
            ssml_gender=texttospeech.SsmlVoiceGender.MALE)

    # Select the type of audio file you want returned
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.LINEAR16)

    # Perform the text-to-speech request on the text input with the selected
    # voice parameters and audio file type
    response = client.synthesize_speech(
        input=synthesis_input, 
        voice=voice, 
        audio_config=audio_config
    )
    
    return io.BytesIO(response.audio_content)
    #audio = AudioSegment(data=io.BytesIO(response.audio_content))
    #play(audio)