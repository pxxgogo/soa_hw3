from django.contrib import admin
from faceBook.models import Face


class FaceAdmin(admin.ModelAdmin):
    fieldsets = [
        ('face_id', {'fields': ['face_id']}),
        ('face', {'fields': ['face']}),

    ]
    list_display = ['face_id']


admin.site.register(Face, FaceAdmin)
