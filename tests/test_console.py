from unittest.mock import Mock

import click.testing
import pytest
import requests
from click.testing import CliRunner
from pytest_mock import MockFixture

from modern_python_setup import console


# fixture to run from command line
@pytest.fixture
def runner() -> CliRunner:
    return click.testing.CliRunner()


# "You should generally have a single assertion per test case, because more fine-grained
# test cases make it easier to figure out why the test suite failed when it does."
# - CLAUDIO JOLOWICZ


def test_main_succeeds(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0


def test_main_prints_title(runner: CliRunner, mock_requests_get: Mock) -> None:
    result = runner.invoke(console.main)
    assert "Lorem Ipsum" in result.output


def test_main_invokes_requests_get(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    assert mock_requests_get.called


def test_main_uses_en_wikipedia_org(runner: CliRunner, mock_requests_get: Mock) -> None:
    runner.invoke(console.main)
    args, _ = mock_requests_get.call_args
    assert "en.wikipedia.org" in args[0]


def test_main_fails_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = Exception("Boom")
    result = runner.invoke(console.main)
    assert result.exit_code == 1


def test_main_prints_message_on_request_error(
    runner: CliRunner, mock_requests_get: Mock
) -> None:
    mock_requests_get.side_effect = requests.RequestException
    result = runner.invoke(console.main)
    assert "Error" in result.output


# fixture to mock wikipedia.random_page
@pytest.fixture
def mock_wikipedia_random_page(mocker: MockFixture) -> Mock:
    return mocker.patch("modern_python_setup.wikipedia.random_page")


def test_main_uses_specified_language(
    runner: CliRunner, mock_wikipedia_random_page: Mock
) -> None:
    runner.invoke(console.main, ["--language=pl"])
    mock_wikipedia_random_page.assert_called_with(language="pl")


# general notes on fakes
# (scaled down functional but not production dependancy, useful if mocks are too
# expensive to implement or too forgiving for errors, e.g. in-memory db):
#
# e.g.
# class FakeAPI:
#     url = "http://localhost:5000/"
#     @classmethod
#     def create(cls):
#         ...
#     def shutdown(self):
#         ...
#
# to test:
#
# wrong: (no tear down -> resource leak)
# @pytest.fixture
# def fake_api():
#     return FakeAPI.create()
#
# correct1: (as generator)(set up & tear down per test function)
# @pytest.fixture
# def fake_api():
#     api = FakeAPI.create()
#     yield api
#     api.shutdown()
#
# correct2: (as generator)(set up & tear down per test session, if set up /
#            tear down expensive )
# @pytest.fixture(scope="session")
# def fake_api():
#     api = FakeAPI.create()
#     yield api
#     api.shutdown()


# use pytest marker to mark tests to skip with -m
# in this case we define end-to-end tests which should be skipped when unit testing
@pytest.mark.e2e
def test_main_succeeds_in_production_env(runner: CliRunner) -> None:
    result = runner.invoke(console.main)
    assert result.exit_code == 0
