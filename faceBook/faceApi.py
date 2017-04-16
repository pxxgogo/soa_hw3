import json
from os import path as op

import cognitive_face as CF

from HW3.settings import BASE_DIR


class FaceAPI(object):
    person_group_id = json.loads(open(op.join(BASE_DIR, 'key.json'), 'r').read())['person_group_id']
    key = json.loads(open(op.join(BASE_DIR, 'key.json'), 'r').read())['key']
    CF.Key.set(key)
    @staticmethod
    def initModel():
        pass
        # try:
        #     info = CF.person_group.get(person_group_id)
        #     print(info)
        # except Exception as e:
        #     CF.person_group.create(person_group_id, 'pxxgogo_soa_hw3')

    @staticmethod
    def create_person(name):
        person_id = CF.person.create(FaceAPI.person_group_id, name)
        CF.person_group.train(FaceAPI.person_group_id)
        return person_id['personId']

    @staticmethod
    def delete_person(person_id):
        CF.person.delete(FaceAPI.person_group_id, person_id)
        CF.person_group.train(FaceAPI.person_group_id)


    @staticmethod
    def get_face(file):
        return CF.face.detect(file)

    @staticmethod
    def add_face(person_id, face):
        face_id = CF.person.add_face(face, FaceAPI.person_group_id, person_id)['persistedFaceId']
        CF.person_group.train(FaceAPI.person_group_id)
        return face_id

    @staticmethod
    def delete_face(person_id, face_id):
        CF.person.delete_face(FaceAPI.person_group_id, person_id, face_id)
        CF.person_group.train(FaceAPI.person_group_id)

    @staticmethod
    def person_group_list():
        return CF.person_group.lists()

    @staticmethod
    def person_group_info():
        return CF.person_group.get(FaceAPI.person_group_id)

    @staticmethod
    def get_person_info(person_id):
        return CF.person.get(FaceAPI.person_group_id, person_id)

    @staticmethod
    def verify_person(face_id, person_id):
        return CF.face.verify(face_id=face_id, person_group_id=FaceAPI.person_group_id, person_id=person_id)