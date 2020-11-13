"""Add a seasoning to an ingredient before you cook it
"""

from abc import ABC
from abc import abstractmethod

class Seasoning(ABC):
    """Seasonings perform their computation in the prep stage
    """

    def __init__(self, **kwargs):
        self.prep(**kwargs)

    @abstractmethod
    def prep(self, **kwargs):
        pass