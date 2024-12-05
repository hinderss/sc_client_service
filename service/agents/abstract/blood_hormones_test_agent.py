from abc import ABC, abstractmethod


class BloodHormonesTestAgent(ABC):
    @abstractmethod
    def execute(self, tsh_val: float, fsh_val: float, lh_val: float, node_lang: str = "rus"):
        pass
