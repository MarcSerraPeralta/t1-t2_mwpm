from typing import Any


from ..setup import Setup


class Model(object):
    def __init__(self, setup: Setup) -> None:
        self._setup = setup

    @property
    def setup(self) -> Setup:
        return self._setup
