# fixtures in this file are discovered by pytest automatically
# no need for test files to explicitly import
from unittest.mock import Mock

import pytest
from _pytest.config import Config
from pytest_mock import MockFixture


# fixture to mock requests.get
@pytest.fixture
def mock_requests_get(mocker: MockFixture) -> Mock:
    mock = mocker.patch("requests.get")
    mock.return_value.__enter__.return_value.json.return_value = {
        "title": "Lorem Ipsum",
        "extract": "Lorem ipsum dolor sit amet",
    }
    return mock


# register the e2e marker using the pytest_configure hook
def pytest_configure(config: Config) -> None:
    config.addinivalue_line("markers", "e2e: mark as end-to-end test.")
