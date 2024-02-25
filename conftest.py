#pytest_plugins = ["core.common_test_utils", "django_extras.tests.common"]
import pytest
from fastapi.testclient import TestClient
from web.main import app
@pytest.fixture(scope='session')
def client():
    yield TestClient(app)
