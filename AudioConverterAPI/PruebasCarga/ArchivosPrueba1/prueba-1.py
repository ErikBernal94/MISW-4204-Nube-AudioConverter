from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2ODg4MDY1OSwianRpIjoiM2RiOWMzNDMtZjJjYi00NDY3LWJiMWQtNjE4YmI0YmZhM2Q0IiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY4ODgwNjU5LCJleHAiOjE2Njg4ODE1NTl9.AgjN3MUBfZz5ayhtB6MF0F4krjISwfsI6F2OYU9QzY0'


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