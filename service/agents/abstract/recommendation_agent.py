from abc import ABC, abstractmethod


class RecommendationAgent(ABC):
    @abstractmethod
    def execute(self, node_name: str):
        pass
