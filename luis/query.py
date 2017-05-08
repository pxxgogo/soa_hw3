import json

import requests
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from os import path as op

from HW3.settings import BASE_DIR, LUIS_PREDICT_URL
import uuid



def query_text(request):
    if request.method == 'GET' and request.user.is_authenticated():
        content = request.GET["content"]
        get_url = "%s\"%s\"" % (LUIS_PREDICT_URL, content)
        response = requests.get(get_url)
        response_content = response.json()
        top_intent_dict = response_content["topScoringIntent"]
        if top_intent_dict["score"] > 0.5:
            intent = top_intent_dict["intent"]
            if intent == "predictValue":
                return JsonResponse({"type": "jump", "url": "/predict_car_price"})
            elif intent == "addFaces":
                return JsonResponse({"type": "jump", "url": "/face_gallery/add_face"})
            elif intent == "manageFaces":
                return JsonResponse({"type": "jump", "url": "/face_gallery"})
            else:
                return JsonResponse({"type": "none"})
        return JsonResponse({"type": "none"})
    elif not request.user.is_authenticated():
        return HttpResponseRedirect("/")


def query_voice(request):
    if request.method == 'POST' and request.user.is_authenticated():
        key = json.loads(open(op.join(BASE_DIR, 'key.json'), 'r').read())['speech_key']
        content = request.FILES.get('data').read()
        access_token = requests.post("https://api.cognitive.microsoft.com/sts/v1.0/issueToken",
                                     headers={
                                         "Content-Length": "0",
                                         "Ocp-Apim-Subscription-Key": key
                                     }
                                     ).text
        print(access_token)
        data = requests.post("https://speech.platform.bing.com/recognize",
                             params={
                                 'scenarios': 'ulm',
                                 'appid': 'D4D52672-91D7-4C74-8AD8-42B1D98141A5',
                                 'locale': 'en-US',
                                 'device.os': 'wp7',
                                 'version': '3.0',
                                 'format': 'json',
                                 'requestid': uuid.uuid4(),
                                 'instanceid': uuid.uuid4(),
                                 "result.profanitymarkup": "0",
                             },
                             headers={
                                 'Content-Type': 'audio/wav; samplerate=16000',
                                 'Authorization': 'Bearer {}'.format(access_token)
                             },
                             data=content)
        try:
            content = data.json()
            txt = sorted(content['results'], key=lambda x: float(
                    x['confidence']))[::-1][0]['lexical']
        except:
            print(data.status_code)
            return JsonResponse({"type": "none"})
        print(txt)
        get_url = "%s\"%s\"" % (LUIS_PREDICT_URL, txt)
        response = requests.get(get_url)
        response_content = response.json()
        top_intent_dict = response_content["topScoringIntent"]
        if top_intent_dict["score"] > 0.5:
            intent = top_intent_dict["intent"]
            if intent == "predictValue":
                return JsonResponse({"type": "jump", "url": "/predict_car_price"})
            elif intent == "addFaces":
                return JsonResponse({"type": "jump", "url": "/face_gallery/add_face"})
            elif intent == "manageFaces":
                return JsonResponse({"type": "jump", "url": "/face_gallery"})
            else:
                return JsonResponse({"type": "none"})
        return JsonResponse({"type": "none"})
    elif not request.user.is_authenticated():
        return HttpResponseRedirect("/")

