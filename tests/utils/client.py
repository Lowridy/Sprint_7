import requests
from faker import Faker

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"

class ScooterClient:
    BASE_URL = BASE_URL
    _fake = Faker("ru_RU")

    def __init__(self):
        self.session = requests.Session()

    def generate_courier_data(self):
        return {
            "login": self._fake.user_name(),
            "password": self._fake.password(length=12, special_chars=False),
            "firstName": self._fake.first_name()
        }

    def register_courier(self, login: str, password: str, first_name: str):
        return self.session.post(
            f"{self.BASE_URL}/courier",
            json={"login": login, "password": password, "firstName": first_name}
        )

    def login_courier(self, login: str, password: str):
        return self.session.post(
            f"{self.BASE_URL}/courier/login",
            json={"login": login, "password": password}
        )

    def delete_courier(self, courier_id: int):
        return self.session.delete(f"{self.BASE_URL}/courier/{courier_id}")

    def create_order(self, **order_data):
        return self.session.post(
            f"{self.BASE_URL}/orders",
            json=order_data
        )

    def get_orders(self):
        return self.session.get(f"{self.BASE_URL}/orders")
