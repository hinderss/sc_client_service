import configparser


class Config:
    config = configparser.ConfigParser()
    config.read("config.ini")

    AGENTS_TO_LOAD = {
        "auth_agent": "service.agents.mock.OstisAuthAgent",
        "navigation_agent": "service.agents.mock.OstisNavigationAgent",
        "recommendation_agent": "service.agents.mock.OstisRecommendationAgent",
        "blood_test_agent": "service.agents.mock.OstisBloodTestAgent",
        "blood_vitamin_agent": "service.agents.mock.OstisBloodVitaminAgent",
        "blood_micronutrients_agent": "service.agents.mock.OstisBloodMicronutrientsAgent",
        "blood_hormones_test_agent": "service.agents.mock.OstisHormonesBloodTestAgent",
    }
    OSTIS_URL = config["DEFAULT"]["ostis_url"]
