from locust import HttpUser, task, between


class HousePriceUser(HttpUser):
    wait_time = between(1, 3)

    @task()
    def create(self):
        request = {
            "area": 1110,
            "bedrooms": 3,
            "bathrooms": 2,
            "stories": 2,
            "mainroad": "yes",
            "guestroom": "no",
            "basement": "yes",
            "hotwaterheating": "yes",
            "airconditioning": "yes",
            "parking": 1,
            "prefarea": "yes",
            "furnishingstatus": "furnished"
            }
        self.client.post("/predict/", json=request)