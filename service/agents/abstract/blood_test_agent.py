from abc import ABC, abstractmethod


class BloodTestAgent(ABC):
    @abstractmethod
    def execute(self, wbc_val: float, rbc_val: float, platelets_val: float, node_lang: str = "rus"):
        pass
