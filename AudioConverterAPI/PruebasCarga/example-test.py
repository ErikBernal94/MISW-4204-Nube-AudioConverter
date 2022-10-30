from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0NjM0OSwianRpIjoiYjVmNzgwM2EtODRkYy00ZTdkLThlNzctNGJiZjE0OTcyYjgzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ2MzQ5LCJleHAiOjE2NjcxNDcyNDl9.LMd1z4yEMvcfWZxsWkHdZ_76J1OTUdrhIVml7JiMe4Q'


class ExampleTest(HttpUser):
    
    wait_time = between(1, 10)

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