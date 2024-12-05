from flask import current_app

from service.agents.abstract.auth_agent import AuthAgent
from service.agents.abstract.blood_analysis import BloodVitaminAgent
from service.agents.abstract.blood_hormones_test_agent import BloodHormonesTestAgent
from service.agents.abstract.blood_micronutrients import BloodMicronutrientsAgent
from service.agents.abstract.blood_test_agent import BloodTestAgent
from service.agents.abstract.navigation_agent import NavigationAgent
from service.agents.abstract.recommendation_agent import RecommendationAgent


def reg_agent(username: str, password: str):
    agent: AuthAgent = current_app.config["agents"]["auth_agent"]
    return agent.reg_agent(username, password)


def auth_agent(username: str, password: str):
    agent: AuthAgent = current_app.config["agents"]["auth_agent"]
    return agent.auth_agent(username, password)


def navigation_agent(node_name: str, node_lang: str):
    agent: NavigationAgent = current_app.config["agents"]["navigation_agent"]
    return agent.execute(node_name, node_lang)


def recommendation_agent(node_name: str):
    agent: RecommendationAgent = current_app.config["agents"]["recommendation_agent"]
    return agent.execute(node_name)


def blood_test_agent(
    wbc_val: float,
    rbc_val: float,
    platelets_val: float,
    node_lang: str = "rus",
):
    agent: BloodTestAgent = current_app.config["agents"]["blood_test_agent"]
    return agent.execute(wbc_val, rbc_val, platelets_val, node_lang)


def blood_hormones_test_agent(
    tsh_val: float,
    fsh_val: float,
    lh_val: float,
    node_lang: str = "rus",
):
    agent: BloodHormonesTestAgent = current_app.config["agents"]["blood_hormones_test_agent"]
    return agent.execute(tsh_val, fsh_val, lh_val, node_lang)


def blood_vitamin_agent(
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
    agent: BloodVitaminAgent = current_app.config["agents"]["blood_vitamin_agent"]
    return agent.execute(
        vitamin_e,
        vitamin_d,
        vitamin_k,
        vitamin_c,
        vitamin_b1,
        vitamin_b2,
        vitamin_b9,
        vitamin_b12,
        vitamin_a,
        vitamin_b6,
    )


def blood_micronutrients_agent(ca_val: float, mg_val: float, fe_val: float):
    agent: BloodMicronutrientsAgent = current_app.config["agents"][
        "blood_micronutrients_agent"
    ]
    return agent.execute(ca_val, mg_val, fe_val)
