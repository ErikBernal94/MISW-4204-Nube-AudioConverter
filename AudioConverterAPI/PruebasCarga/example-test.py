from locust import HttpUser, task

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0NDQxMiwianRpIjoiODBjYzI1OTEtMzQ4MC00MDllLTk4NjEtOTE0OGU0ZjIwZjVjIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ0NDEyLCJleHAiOjE2NjcxNDUzMTJ9.aQ_QU0DEqzxGZJePqhWRHVSARqtIU2kthuUCk-M1mrQ'


class ExampleTest(HttpUser):

    @task
    def submit(self):
        print('entro al testtt')
        attach = open('voz.mp3', 'rb')
        r = self.client.post("http://127.0.0.1:5000/api/tasks", {
           'Authentication': 'Bearer '+ token,
           'newFormat': 'm4a',
           'docfile': attach,
        })
        print(r)