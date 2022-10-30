from locust import HttpUser, task, between
import requests
import random
token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjUzOTE5OSwianRpIjoiM2JlYmYwN2EtYzdmYi00NTk2LWJiYzMtMjdlOTk5ZjNmMmVjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY2NTM5MTk5LCJleHAiOjE2NjY1NDAwOTl9.6RKA7npMqrpCdHRUmE_2ZtyVmCXs436TzZ52t1pWlZI'


class ExampleTest(HttpUser):
    # @task
    # def home(self):
    #     self.client.request(method="GET", url="/home")
    wait_time = between(1, 3)
    def on_start(self):
        """ on_start is called when a Locust start before any task is scheduled """
        self.login()

    def login(self):
        print('entro al login')
        post_data = {'username':'admin', 'password':'admin2022'}
        response = self.client.post('http://127.0.0.1:5000/api/auth/login', post_data, catch_response=True)
        print('respondio')
        print(response.body)
        token = response.body.token
            
    @task
    def submit(self):
        print('entro al testtt')
        headers = {"Authorization": "Bearer " + token}
        numberFile = random.randint(1, 30)
        nameFile = 'voz'+'.mp3'
        print(nameFile)
        myfile = {'file': (nameFile, open(nameFile, 'rb'),'application/octet-stream')}
        payload={
            "newFormat": "m4a"
        }
        r = self.client.post("http://127.0.0.1:5000/api/tasks",headers=headers, files=myfile ,data=payload, verify=False)