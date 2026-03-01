import pytest

from app.settings import Setting


@pytest.fixture
def settings():
    return Setting()