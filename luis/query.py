from django.http import JsonResponse
from HW3.settings import LUIS_PREDICT_URL
from django.http import HttpResponseRedirect
import requests


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
