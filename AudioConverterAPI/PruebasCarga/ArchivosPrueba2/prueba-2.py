from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODg5MjEwMywianRpIjoiNjU1ZjE3MjItMDNjZC00NTU2LTkwNTYtNzQzMjFlMWQ5YmJlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4ODkyMTAzLCJleHAiOjE2Njg4OTMwMDN9.kfzsP3eskXdIw-VPkCdIy0NS4v_7bg8bPEwanmCT3n8'


class ExampleTest(HttpUser):

    # wait_time = between(1, 2)
    @task
    def submit(self):
        print('entro al testtt')
        headers = {"Authorization": "Bearer " + token}
        numberFile = random.randint(1, 30)
        nameFile = 'Song'+str(numberFile)+'.mp3'
        print(nameFile)
        myfile = {'file': (nameFile, open(nameFile, 'rb'),'application/octet-stream')}
        payload={
            "newFormat": "wav"
        }
        r = self.client.post("http://35.206.74.89:5000/api/tasks",headers=headers, files=myfile ,data=payload, verify=False)