from abc import ABC, abstractmethod


class BloodMicronutrientsAgent(ABC):
    @abstractmethod
    def execute(self, ca_val: float, mg_val: float, fe_val: float):
        pass
