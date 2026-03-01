import pytest
from faker import Factory as FakerFactory

@pytest.fixture()
def faker():
    return FakerFactory.create()