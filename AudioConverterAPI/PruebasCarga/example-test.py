from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0NzY3NiwianRpIjoiZGQxY2I3ZDctNDQyNC00ODJlLTgzMGUtYzg3MGNiYmU4M2VkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ3Njc2LCJleHAiOjE2NjcxNDg1NzZ9.gMY-xXV1htL4-klmLY-61YpjCfoS_LYEfKDsVPVxZdk'


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