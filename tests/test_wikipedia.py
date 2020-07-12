import click.testing
import pytest

from modern_python_setup import wikipedia


def test_random_page_uses_given_language(mock_requests_get):
    wikipedia.random_page(language="de")
    args, _ = mock_requests_get.call_args
    assert "de.wikipedia.org" in args[0]


def test_random_page_returns_page(mock_requests_get):
    page = wikipedia.random_page()
    assert isinstance(page, wikipedia.Page)


def test_random_page_handles_validation_errors(mock_requests_get):
    # test what happens if None is returned as JSON obj (by wikipedia)
    # schema validation should fail
    mock_requests_get.return_value.__enter__.return_value.json.return_value = None
    # assert click.ClickException would be raised
    with pytest.raises(click.ClickException):
        wikipedia.random_page()


def test_trigger_typeguard(mock_requests_get):
    # test to fail typeguard on purpose
    import json

    # this will pass static type checkers as values loaded from JSON are hard to chk
    data = json.loads('{ "language": 1 }')
    wikipedia.random_page(language=data["language"])
