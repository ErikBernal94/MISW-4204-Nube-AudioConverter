from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE1MjYyOSwianRpIjoiMGVjZmU2NzAtZTY3OS00NmUwLTgzY2UtOGZlNTRhZTkyYTVhIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTUyNjI5LCJleHAiOjE2NjcxNTM1Mjl9.4wkGh8u0daYtxD6TC3L2sBvWrFObVTtr4E18UHzTU7A'


class ExampleTest(HttpUser):

    # wait_time = between(1, 10)

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
        r = self.client.post("http://35.222.194.77:5000/api/tasks",headers=headers, files=myfile ,data=payload, verify=False)