import requests
from faker import Faker

BASE_URL = "https://qa-scooter.praktikum-services.ru/api/v1"
fake = Faker("ru_RU")

class ScooterClient:
    BASE_URL = BASE_URL  

    def __init__(self):
        self.session = requests.Session()

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

    def create_order(self, **order_data):
        return self.session.post(
            f"{self.BASE_URL}/orders",
            json=order_data
        )

    def get_orders(self):
        return self.session.get(f"{self.BASE_URL}/orders")


def register_new_courier_and_return():
    login = fake.user_name()
    password = fake.password(length=12, special_chars=False)
    first_name = fake.first_name()
    resp = ScooterClient().register_courier(login, password, first_name)
    if resp.status_code == 201:
        return {"login": login, "password": password, "firstName": first_name}
    return {}
