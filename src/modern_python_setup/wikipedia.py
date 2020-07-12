from dataclasses import dataclass

import click
import desert
import marshmallow
import requests

# the url now accepts different language specified by user
API_URL: str = "https://{language}.wikipedia.org/api/rest_v1/page/random/summary"


# class to define structure on wikipedia returned page
@dataclass
class Page:
    title: str
    extract: str


# generate schema to serialize / deserialize / validate page obj to / from page JSON
# (from class definition)
# "meta=..." used to ignore unknow / undefined fields (keys / values)
schema = desert.schema(Page, meta={"unknown": marshmallow.EXCLUDE})


def random_page(language: str = "en") -> Page:
    url = API_URL.format(language=language)

    try:
        with requests.get(url) as response:
            response.raise_for_status()
            data = response.json()
            # schema.load(data) -> use schema to load data
            return schema.load(data)
    except requests.RequestException as error:
        # handle requests exception gracefully, raise as click exception
        message = str(error)
        raise click.ClickException(message)
