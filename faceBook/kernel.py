# coding=utf8
from cStringIO import StringIO

from PIL import Image
from django.core.files.base import ContentFile
from django.http import HttpResponseRedirect
from django.http import JsonResponse

from faceApi import FaceAPI
from faceBook.models import FaceTempPhoto, Face, Tempfaces
from datetime import datetime
import re
import os

from HW3.settings import TEMP_PHOTO_DIR


def upload_face_photo(request):
    if not request.user.is_active:
        return HttpResponseRedirect("/")
    temp_photo = FaceTempPhoto()
    # print(request.FILES)
    temp_photo.photo = request.FILES["file[]"]
    try:
        info = FaceAPI.get_face(temp_photo.photo)
    except Exception as e:
        print(e)
        return JsonResponse({"return_code": 1, "faces": []})
    if len(info) == 0:
        print("No faces")
        return JsonResponse({"return_code": 1, "faces": []})
    temp_photo.save()
    img = Image.open(temp_photo.photo)
    # try:
    #     exif = imageInfo["exif_orientation"]
    #     print exif
    # except:
    #     exif = 1
    #     print ("No rotate")
    # if exif == 2:
    #     imgRotate = img.transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 3:
    #     imgRotate = img.transpose(Image.ROTATE_180)
    # elif exif == 4:
    #     imgRotate = img.transpose(Image.FLIP_TOP_BOTTOM)
    # elif exif == 5:
    #     imgRotate = img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 6:
    #     imgRotate = img.transpose(Image.ROTATE_270)
    # elif exif == 7:
    #     imgRotate = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 8:
    #     imgRotate = img.transpose(Image.ROTATE_90)
    # else:
    #     imgRotate = img
    face_list = []
    temp_faces = Tempfaces()
    temp_faces.temp_photo = temp_photo
    # print(temp_photo)
    temp_faces.save()
    for face in info:
        face_id = face["faceId"]
        top = face["faceRectangle"]["top"]
        left = face["faceRectangle"]['left']
        width = face["faceRectangle"]["width"]
        height = face["faceRectangle"]["height"]

        existed_face_list = Face.objects.filter(face_id=face_id)
        if (len(existed_face_list) > 0):
            face_model = existed_face_list[0]
        else:
            face_model = Face()
            face_model.face_id = face_id
            face_part = img.crop((left, top, left + width, top + height))
            f = StringIO()
            try:
                face_part.save(f, format='png')
                s = f.getvalue()
                face_model.face.save(face_id + ".png", ContentFile(s))
                face_model.save()
                temp_faces.face_list.add(face_model)
            finally:
                f.close()
        face_to_frontend = {}
        face_to_frontend["face_No"] = face_model.id
        try:
            face_to_frontend["face_data_src"] = "data:image/jpg;base64,%s" % open(face_model.face.path,
                                                                                  'rb').read().encode(
                "base64")
        except IOError:
            face_to_frontend["face_data_src"] = "#"
        face_list.append(face_to_frontend)
    return JsonResponse({"return_code": 0, "faces": face_list}, safe=False)


def ensure_adding_face(request):
    if not request.user.is_active:
        return HttpResponseRedirect("/login")
    user = request.user
    face_No = request.POST["face_id"]
    try:
        face = Face.objects.get(id=face_No)
    except Exception as e:
        print(e)
        return JsonResponse({"return_code": 1}, safe=False)
    if len(face.user_face.all()) > 0:
        return JsonResponse({"return_code": 2}, safe=False)

    try:
        persisted_face_id = FaceAPI.add_face(user.person_id, face.face.path)
        print(persisted_face_id)
    except Exception as e:
        print(e)
        return JsonResponse({"return_code": 4}, safe=False)
    face.face_id = persisted_face_id
    face.save()
    user.face_book.add(face)
    user.save()
    temp_faces_list = face.tempfaces.all()
    if len(temp_faces_list) > 0:
        temp_faces = temp_faces_list[0]
        for face_temp in temp_faces.face_list.all():
            if face == face_temp:
                continue
            face.face.delete()
            face.delete()
        temp_faces.temp_photo.photo.delete()
        temp_faces.temp_photo.delete()
        temp_faces.delete()
    return JsonResponse({"return_code": 0}, safe=False)




def ensure_deleting_face(request):
    if not request.user.is_active:
        return HttpResponseRedirect("/")
    face_id = request.POST["face_id"]
    try:
        face = Face.objects.get(id=face_id)
    except:
        return JsonResponse({"return_code": 1}, safe=False)
    if len(request.user.face_book.filter(id=face_id)) == 0:
        return JsonResponse({"return_code": 2}, safe=False)
    try:
        FaceAPI.delete_face(request.user.person_id, face.face_id)
    except:
        return JsonResponse({"return_code": 4}, safe=False)
    face.face.delete()
    face.delete()
    return JsonResponse({"return_code": 0}, safe=False)


def send_captured_photo(request):
    if not request.user.is_active:
        return HttpResponseRedirect("/")
    imgstring = request.POST['img_data']
    # print(imgstring)
    image_data = re.sub('^data:image/.+;base64,', '', imgstring).decode('base64')
    output = StringIO()
    output.write(image_data)
    content = ContentFile(output.getvalue())
    now = datetime.now()
    file_name = str(now) + ".jpg"
    temp_photo = FaceTempPhoto()
    temp_photo.photo.save(file_name, content)
    try:
        info = FaceAPI.get_face(temp_photo.photo)
    except Exception as e:
        print(e)
        return JsonResponse({"return_code": 1, "faces": []})
    if len(info) == 0:
        print("No faces")
        return JsonResponse({"return_code": 1, "faces": []})
    temp_photo.save()
    img = Image.open(temp_photo.photo)
    # try:
    #     exif = imageInfo["exif_orientation"]
    #     print exif
    # except:
    #     exif = 1
    #     print ("No rotate")
    # if exif == 2:
    #     imgRotate = img.transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 3:
    #     imgRotate = img.transpose(Image.ROTATE_180)
    # elif exif == 4:
    #     imgRotate = img.transpose(Image.FLIP_TOP_BOTTOM)
    # elif exif == 5:
    #     imgRotate = img.transpose(Image.ROTATE_270).transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 6:
    #     imgRotate = img.transpose(Image.ROTATE_270)
    # elif exif == 7:
    #     imgRotate = img.transpose(Image.ROTATE_90).transpose(Image.FLIP_LEFT_RIGHT)
    # elif exif == 8:
    #     imgRotate = img.transpose(Image.ROTATE_90)
    # else:
    #     imgRotate = img
    face_list = []
    temp_faces = Tempfaces()
    temp_faces.temp_photo = temp_photo
    # print(temp_photo)
    temp_faces.save()
    for face in info:
        face_id = face["faceId"]
        top = face["faceRectangle"]["top"]
        left = face["faceRectangle"]['left']
        width = face["faceRectangle"]["width"]
        height = face["faceRectangle"]["height"]

        existed_face_list = Face.objects.filter(face_id=face_id)
        if (len(existed_face_list) > 0):
            face_model = existed_face_list[0]
        else:
            face_model = Face()
            face_model.face_id = face_id
            face_part = img.crop((left, top, left + width, top + height))
            f = StringIO()
            try:
                face_part.save(f, format='png')
                s = f.getvalue()
                face_model.face.save(face_id + ".png", ContentFile(s))
                face_model.save()
                temp_faces.face_list.add(face_model)
            finally:
                f.close()
        face_to_frontend = {}
        face_to_frontend["face_No"] = face_model.id
        try:
            face_to_frontend["face_data_src"] = "data:image/jpg;base64,%s" % open(face_model.face.path,
                                                                                  'rb').read().encode(
                "base64")
        except IOError:
            face_to_frontend["face_data_src"] = "#"
        face_list.append(face_to_frontend)
    return JsonResponse({"return_code": 0, "faces": face_list}, safe=False)
