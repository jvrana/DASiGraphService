import pytest
from webtest import TestApp

from DASiGraph.app import create_app
from DASiGraph.config import TestConfig
import os

@pytest.yield_fixture(scope="function")
def app():
    """An application for the tests."""
    _app = create_app(TestConfig)

    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope="function")
def testapp(app):
    """A Webtest app."""
    return TestApp(app)

@pytest.fixture
def here():
    return os.path.abspath(os.path.dirname(__file__))