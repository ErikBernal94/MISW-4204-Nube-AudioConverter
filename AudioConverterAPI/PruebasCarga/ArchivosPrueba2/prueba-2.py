from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE1NDI1NCwianRpIjoiNDJmODkxMjAtMDNlYi00OTk1LTk2MWUtMTU0MWEyOTg5MTI1IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTU0MjU0LCJleHAiOjE2NjcxNTUxNTR9.1pGPeFc3usrGrMym_h94F0iaX8wrJq-okVZef0Ci6lk'


class ExampleTest(HttpUser):

    wait_time = between(1, 2)
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