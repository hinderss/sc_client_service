from abc import ABC, abstractmethod


class DiagnosisAgent(ABC):
    @abstractmethod
    def execute(self, symptoms: list):
        pass
