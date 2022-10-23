from locust import HttpUser, task

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NjQ3OTgzNCwianRpIjoiMjZhNjZlNTQtZjM2ZC00NDBjLTkyZDItMDczOGY2NDJhZGZlIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MSwibmJmIjoxNjY2NDc5ODM0LCJleHAiOjE2NjY0ODA3MzR9.whkNm5ERcwKSepe8NKuun-RHPfwpgNbcvGWplwMafI4'


class ExampleTest(HttpUser):

    @task
    def submit(self):
        print('entro al testtt')
        attach = open('audio.mp3', 'rb')
        r = self.client.post("http://127.0.0.1:5000/api/tasks", {
           'Authentication': 'Bearer '+ token,
           'newFormat': 'm4a',
           'docfile': attach,
        })
        print(r)