import pytest
from tests.utils.client import ScooterClient

@pytest.fixture(scope="session")
def client():
    return ScooterClient()

@pytest.fixture
def new_courier(client):
    data = client.generate_courier_data()
    resp = client.register_courier(**data)
    if resp.status_code != 201:
        pytest.skip("Не удалось зарегистрировать курьера")
    return data
