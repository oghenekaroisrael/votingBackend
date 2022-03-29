import json
import requests
from django.conf import settings

class FacialRecognitionMiddleware():
    def newPerson(self, request, exception):
        req = json.loads(request.body)
        url = "https://api.luxand.cloud/subject/v2"

        payload = {"name":"from rq","store":"1", "photo": req["photo"]}

        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }

        files = {}

        response = requests.request("POST", url, data=payload, headers=headers, files=files)

        print(response.text)
    
    def addFace(self, request, exception):
        req = json.loads(request.body)
        user_id = req["userId"]
        url = "https://api.luxand.cloud/subject/"+user_id
        payload = {"store":"1", "photo": req["photo"]}
        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
        files = {}
        response = requests.request("POST", url, data=payload, headers=headers, files=files)

        print(response.text)
    
    def verifyFace(self, request, exception):
        req = json.loads(request.body)
        user_id = req["userId"]
        url = "https://api.luxand.cloud/photo/verify/"+user_id
        payload = {"photo": req["photo"]}
        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
        files = {}
        response = requests.request("POST", url, data=payload, headers=headers, files=files)
        print(response.text)
    
    def recogniseFace(self, request, exception):
        req = json.loads(request.body)
        url = "https://api.luxand.cloud/photo/search"
        payload = { "photo": req["photo"] }
        headers = { 'token': "b4a771e51ce54de2a65841db6d8259f1" }
        files = {}
        response = requests.request("POST", url, data=payload, headers=headers, files=files)
        print(response.text)
