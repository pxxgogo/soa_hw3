import StringIO
import re

from django.contrib import auth
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render

from faceBook.faceApi import FaceAPI
from faceBook.models import FaceTempPhoto
from models import AccountUser


def login(request):
    if request.method == 'POST' and not request.user.is_authenticated():
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
            # Correct password, and the user is marked "active"
            auth.login(request, user)
            # Redirect to a success page.
            return HttpResponseRedirect("/")
        else:
            return render(request, "login.html", {"error_info": "Fail to login the account."})
    else:
        if not request.user.is_authenticated():
            return render(request, "login.html", {})
        else:
            return HttpResponseRedirect("/")


def login_with_updated_photo(request):
    if request.method == 'POST' and not request.user.is_authenticated():
        username = request.POST['username']
        temp_photo = FaceTempPhoto()
        # print(request.FILES)
        temp_photo.photo = request.FILES["file[]"]
        try:
            info = FaceAPI.get_face(temp_photo.photo)
        except Exception as e:
            print(e)
            return JsonResponse({"return_code": 1})
        if len(info) == 0:
            print("No faces")
            return JsonResponse({"return_code": 1})
        if len(info) > 1:
            print("over one faces")
            return JsonResponse({"return_code": 2})
        face = info[0]
        try:
            user = AccountUser.objects.get(username=username)
        except Exception as e:
            return JsonResponse({"return_code": 4})
        face_id = face["faceId"]
        print(face_id)
        verify_info = FaceAPI.verify_person(face_id, user.person_id)
        print(verify_info)
        is_identical = verify_info["isIdentical"]
        confidence = verify_info["confidence"]
        if is_identical:
            auth.login(request, user)
            return JsonResponse({"return_code": 0}, safe=False)
        return JsonResponse({"return_code": 3}, safe=False)


def login_with_captured_photo(request):
    if request.method == 'POST' and not request.user.is_authenticated():
        username = request.POST['username']
        imgstring = request.POST['img_data']
        image_data = re.sub('^data:image/.+;base64,', '', imgstring).decode('base64')
        output = StringIO.StringIO()
        output.write(image_data)
        try:
            info = FaceAPI.get_face(ContentFile(output.getvalue()))
        except Exception as e:
            print(e)
            return JsonResponse({"return_code": 1})
        if len(info) == 0:
            print("No faces")
            return JsonResponse({"return_code": 1})
        if len(info) > 1:
            print("over one faces")
            return JsonResponse({"return_code": 2})
        face = info[0]
        try:
            user = AccountUser.objects.get(username=username)
        except Exception as e:
            return JsonResponse({"return_code": 4})
        face_id = face["faceId"]
        print(face_id)
        verify_info = FaceAPI.verify_person(face_id, user.person_id)
        print(verify_info)
        is_identical = verify_info["isIdentical"]
        confidence = verify_info["confidence"]
        if is_identical:
            auth.login(request, user)
            return JsonResponse({"return_code": 0}, safe=False)
        return JsonResponse({"return_code": 3}, safe=False)
