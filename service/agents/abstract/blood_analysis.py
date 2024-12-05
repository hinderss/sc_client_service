from abc import ABC, abstractmethod


class BloodVitaminAgent(ABC):
    @abstractmethod
    def execute(
        self,
        vitamin_e: float,
        vitamin_d: float,
        vitamin_k: float,
        vitamin_c: float,
        vitamin_b1: float,
        vitamin_b2: float,
        vitamin_b9: float,
        vitamin_b12: float,
        vitamin_a: float,
        vitamin_b6: float,
    ):
        pass
