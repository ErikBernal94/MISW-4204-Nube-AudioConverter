from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0ODY1MywianRpIjoiYTVmZmM4MDctMTg0NC00N2RlLTg0ZjQtMDQ3YjhiZWNkYjkzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ4NjUzLCJleHAiOjE2NjcxNDk1NTN9.CYgZhoxwtSDnieRmzIaUfRp2rUSQwpTrHJ3q94Va7CE'


class ExampleTest(HttpUser):

    # wait_time = between(1, 10)

    @task
    def submit(self):
        print('entro al testtt')
        headers = {"Authorization": "Bearer " + token}
        numberFile = random.randint(1, 30)
        nameFile = 'voz'+'.mp3'
        print(nameFile)
        myfile = {'file': (nameFile, open(nameFile, 'rb'),'application/octet-stream')}
        payload={
            "newFormat": "wav"
        }
        r = self.client.post("http://35.222.194.77:5000/api/tasks",headers=headers, files=myfile ,data=payload, verify=False)