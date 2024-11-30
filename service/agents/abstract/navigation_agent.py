from abc import ABC, abstractmethod


class NavigationAgent(ABC):
    @abstractmethod
    def execute(self, node_name: str, node_lang: str) -> None:
        pass

