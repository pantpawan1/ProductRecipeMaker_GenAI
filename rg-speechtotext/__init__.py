import pdb
import os
import logging
import azure.functions as func
import azure.cognitiveservices.speech as speech

def main(req: func.HttpRequest) -> func.HttpResponse:
    speech_key = os.environ["SpeechServiceKey"]
    service_region = os.environ["SpeechServiceRegion"]

    audio_data = req.get_body()

    speech_config = speech.SpeechConfig(subscription=speech_key, region=service_region)
    audio_config = speech.AudioConfig(filename="C:\\Users\\XJ768PU\\OneDrive - EY\\Documents\\Sound recordings\\Recording.mp3", stream=audio_data)

    speech_recognizer = speech.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)

    result = speech_recognizer.recognize_once()

    if result.reason == speech.ResultReason.RecognizedSpeech:
        recognized_text = result.text
    else:
        recognized_text = ""

    return func.HttpResponse(f"Recognized text: {recognized_text}")
