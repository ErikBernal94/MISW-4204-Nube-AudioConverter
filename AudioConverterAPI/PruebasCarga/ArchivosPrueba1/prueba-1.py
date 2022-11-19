from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODg3MTAwMCwianRpIjoiZDExNWJiNzUtMzRkYS00MGIzLWJmZWEtMjM1MThhZGY4NTcxIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4ODcxMDAwLCJleHAiOjE2Njg4NzE5MDB9.Esg2k_WAHCBYCU0dTbvzdk5EzpUPScyDAE6iR2TCxu0'


class ExampleTest(HttpUser):

    # wait_time = between(1, 2)
    @task
    def submit(self):
        print('entro al testtt')
        headers = {"Authorization": "Bearer " + token}
        numberFile = random.randint(1, 30)
        nameFile = 'voz'+str(numberFile)+'.m4a'
        print(nameFile)
        myfile = {'file': (nameFile, open(nameFile, 'rb'),'application/octet-stream')}
        payload={
            "newFormat": "mp3"
        }
        r = self.client.post("http://35.206.74.89:5000/api/tasks",headers=headers, files=myfile ,data=payload, verify=False)