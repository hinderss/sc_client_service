import configparser


class Config:
    config = configparser.ConfigParser()
    config.read("config.ini")

    AGENTS_TO_LOAD = {
        "auth_agent": "service.agents.ostis.OstisAuthAgent",
        "navigation_agent": "service.agents.ostis.OstisNavigationAgent",
        "recommendation_agent": "service.agents.ostis.OstisRecommendationAgent",
        "blood_test_agent": "service.agents.ostis.OstisBloodTestAgent",
        "blood_analysis_agent": "service.agents.ostis.OstisBloodAnalysisAgent",
        "blood_micronutrients_agent": "service.agents.ostis.OstisBloodMicronutrientsAgent",
    }
    OSTIS_URL = config["DEFAULT"]["ostis_url"]
