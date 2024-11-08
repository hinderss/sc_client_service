from abc import ABC, abstractmethod


class AuthAgent(ABC):
    @abstractmethod
    def reg_agent(self, username: str, password: str) -> None:
        pass

    @abstractmethod
    def auth_agent(self, username: str, password: str) -> None:
        pass
