from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODkwNTQ3NSwianRpIjoiODIyMDhiNWItZDQ3NC00OWU4LWJkN2EtZTlkNDAwMzMyZGY1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4OTA1NDc1LCJleHAiOjE2Njg5MDYzNzV9.z8WW8fmDG4HQ_45cNlB8HjcfuEjM9Sp6WxkDP8vVc3g'


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