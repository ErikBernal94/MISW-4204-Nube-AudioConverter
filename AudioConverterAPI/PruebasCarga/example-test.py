from locust import HttpUser, task, between
import requests
import random

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0OTYxNSwianRpIjoiYjVlMTk3NzItMDgwNy00NjU2LTlkY2EtMzZjYWY2MGY0M2MzIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ5NjE1LCJleHAiOjE2NjcxNTA1MTV9.dgDlLPccTpVMrV0cWjvpWrcAjBa_yRYTUIPNNWu7LCU'


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