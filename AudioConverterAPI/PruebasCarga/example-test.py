from locust import HttpUser, task

token ='eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTY2NzE0NDU4MiwianRpIjoiZDBhMzQ0ODYtZDllZi00MDBhLWE3MmQtNjY2YzAzMTZiOTRkIiwidHlwZSI6ImFjY2VzcyIsInN1YiI6MiwibmJmIjoxNjY3MTQ0NTgyLCJleHAiOjE2NjcxNDU0ODJ9._tFLEnKZvzew8UpDZAYyG5IBOpTm9oT27pEqlrzqqJg'


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