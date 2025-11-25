from typing import Any

import factory


def lazy_function_factory(value: Any, max_length: int = 20) -> factory.LazyFunction:
    return factory.LazyFunction(lambda: value()[:max_length])
