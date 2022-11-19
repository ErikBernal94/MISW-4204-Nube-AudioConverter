from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODg3MDAyNywianRpIjoiZDAwNDVlMjEtNzQwNC00ZDg1LWJmZjAtMWNhNzUzNmM4MDI2IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4ODcwMDI3LCJleHAiOjE2Njg4NzA5Mjd9.59g1uE-cJqsVNTgwFnLT9727WZALbzlK8_zTl2YArvA'


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