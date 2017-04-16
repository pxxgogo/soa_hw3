"""HW3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

import account.login
import account.views
import account.register
import faceBook.views
import faceBook.kernel

urlpatterns = [
                  url(r'^admin/', admin.site.urls),
                  url(r'^$', account.views.index),
                  url(r'^logout$', account.views.logout),
                  url(r'^login$', account.login.login),
                  url(r'^register$', account.register.register),
                  url(r'^face_gallery$', faceBook.views.face_gallery_view),
                  url(r'^face_gallery/add_face$', faceBook.views.add_face_view),
                  url(r'^face_gallery/send_face$', faceBook.kernel.upload_face_photo),
                  url(r'^face_gallery/ensure_adding_face$', faceBook.kernel.ensure_adding_face),
                  url(r'^face_gallery/ensure_deleting_face$', faceBook.kernel.ensure_deleting_face),
                  url(r'^login_with_updated_photo$', account.login.login_with_updated_photo),
                  url(r'^login_with_captured_photo$', account.login.login_with_captured_photo),
                  url(r"^face_gallery/send_captured_photo$", faceBook.kernel.send_captured_photo)

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
