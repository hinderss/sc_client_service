from .abstract.auth_agent import AuthAgent, RegStatus, AuthStatus
from .abstract.blood_test_agent import BloodTestAgent
from .abstract.navigation_agent import NavigationAgent
from .abstract.recommendation_agent import RecommendationAgent


class OstisAuthAgent(AuthAgent):
    def reg_agent(self, username: str, password: str):
        print(f"MockAgent: Pretend registering {username} - {password}")
        return {"status": RegStatus.CREATED}

    def auth_agent(self, username: str, password: str):
        print(f"MockAgent: Pretend authenticating {username} - {password}")
        return {
            "status": AuthStatus.INVALID,
            "message": "Invalid credentials",
        }


class OstisBloodTestAgent(BloodTestAgent):

    def execute(self, wbc_val: float, rbc_val: float, platelets_val: float, node_lang: str = "rus"):
        return {"message": "some_message"}


class OstisRecommendationAgent(RecommendationAgent):
    def execute(self, node_name: str):
        return {"message": "some_message"}


class OstisNavigationAgent(NavigationAgent):
    def execute(self, node_name: str, node_lang: str = "rus"):
        return {"message": "some_message"}


