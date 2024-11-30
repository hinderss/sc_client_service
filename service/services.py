from flask import current_app

from service.agents.abstract.auth_agent import AuthAgent
from service.agents.abstract.blood_test_agent import BloodTestAgent
from service.agents.abstract.navigation_agent import NavigationAgent
from service.agents.abstract.recommendation_agent import RecommendationAgent



def reg_agent(username: str, password: str):
    agent: AuthAgent = current_app.config['agents']['auth_agent']
    return agent.reg_agent(username, password)


def auth_agent(username: str, password: str):
    agent: AuthAgent = current_app.config['agents']['auth_agent']
    return agent.auth_agent(username, password)

def navigation_agent(node_name: str, node_lang: str):
    agent: NavigationAgent = current_app.config['agents']['navigation_agent']
    return agent.execute(node_name, node_lang)

def recommendation_agent(node_name: str):
    agent: RecommendationAgent = current_app.config['agents']['recommendation_agent']
    return agent.execute(node_name)

def blood_test_agent(wbc_val: float, rbc_val: float,
                     platelets_val: float, node_lang: str = "rus"):
    agent: BloodTestAgent = current_app.config['agents']['blood_test_agent']
    return agent.execute(wbc_val, rbc_val, platelets_val, node_lang)


