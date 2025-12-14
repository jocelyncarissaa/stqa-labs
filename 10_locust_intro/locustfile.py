from locust import HttpUser, task, between

class HitCounterUser(HttpUser):
    host = "http://localhost:5003"
    #Setelah melakukan 1 task, akan diam dulu selama 3-5 detik baru lanjut ke task selanjutnya
    #Tanpa wait time, requets akan dikriim secepat CPU (tidak masuk akal)
    wait_time = between(3, 5)

    #Weight
    #Tujuan: sesuai dengan perilaku nyata
    #Total bobot: 1 + 3 = 4
    #3x -> /hit
    #1x -> /

    #Aksi user: membuka homepage
    #Harus di tes karena homepage selalu menjadi entry point, walaupun bukan transaksi utama
    @task (1)
    def load_homepage(self):
        self.client.get("/")
    
    #Aksi user: klik tombol 
    @task(3)
    def post_hit(self):
        self.client.post("/hit")