# fixtures in this file are discovered by pytest automatically
# no need for test files to explicitly import
import pytest


# fixture to mock requests.get
@pytest.fixture
def mock_requests_get(mocker):
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


# register the e2e marker using the pytest_configure hook
def pytest_configure(config):
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
