import pytest
from app import create_app

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('testing')

    # Establish an application context
    with flask_app.test_client() as testing_client:
        # Establish an application context
        with flask_app.app_context():
            yield testing_client