from locust import HttpUser, task, SequentialTaskSet, between
import random
import time

#Batas toleransi waktu respon
#Kalau halaman / lebih dari 3 detik, maka dianggap FAIL, walaupun status 200
RESPONSE_TIME_LIMIT_MS = 3000.0

#1 user locust akan menjalankan task dibawah ini secara berurutan
class PetShopWorkflow(SequentialTaskSet):
    #This task will always run FIRST because the TaskSet is Sequential
    @task
    def add_new_pet(self):
        #Membuat nama hewan secara acak
        pet_name = f"Fluffy-{random.randint(1, 10000)}"

        #Tujuan: setiap user -> data berbeda, murni load + stress database
        self.client.post("/pets", json={
            "name": pet_name,
            "category": "dog"
        })

    #This task always run SECOND
    @task
    def load_homepage(self):
        #Hitung waktu respon manual
        #Dipakai untuk mengukur berapa lama homepage loading
        start_time = time.time()

        #catch_response = True supaya bisa override
        #Request yang status 200 tetap bisa dianggap FAIL
        with self.client.get("/", catch_response = True) as response:
            #Hitung response time dalam ms
            response_time_ms = (time.time() - start_time) * 1000

            #Kalau lebih dari 3 detik > request dicatat FAIL
            if response_time_ms > RESPONSE_TIME_LIMIT_MS:
                response.failure(f"Response time exceeded {RESPONSE_TIME_LIMIT_MS}ms: ({response_time_ms:.0f}ms)")

            #Kalau bukan 200 > dicatat FAIL    
            elif response.status_code != 200:
                response.failure(f"Got non-200 status code: {response.status_code}")

            #Kalau aman    
            else:
                response.success()
        self.client.get("/")

class PetShopUser(HttpUser):
    host = "http://127.0.0.1:5004"

    #Tidak ada jeda > stress
    wait_time = between (0, 0)
    tasks = [PetShopWorkflow]