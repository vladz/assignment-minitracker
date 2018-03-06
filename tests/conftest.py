import pytest

from minitracker import app


@pytest.fixture
def cli(loop, aiohttp_client):
    test_app = app.init()
    return loop.run_until_complete(aiohttp_client(test_app))
