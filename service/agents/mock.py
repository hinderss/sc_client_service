from .abstract.auth_agent import AuthAgent


class OstisAuthAgent(AuthAgent):
    def reg_agent(self, username: str, password: str) -> None:
        print(f"MockAgent: Pretend registering {username} - {password}")

    def auth_agent(self, username: str, password: str) -> None:
        print(f"MockAgent: Pretend authenticating {username} - {password}")
