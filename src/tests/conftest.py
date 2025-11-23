import punq
import pytest

from src.project.containers import get_container


@pytest.fixture
def container() -> punq.Container:
    return get_container()
