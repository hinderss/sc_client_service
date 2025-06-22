import configparser


class Config:
    config = configparser.ConfigParser()
    config.read("config.ini")

    AGENTS_TO_LOAD = {
        "auth_agent": "service.agents.mock.OstisAuthAgent",
        "navigation_agent": "service.agents.ostis.OstisNavigationAgent",
        "recommendation_agent": "service.agents.ostis.OstisRecommendationAgent",
        "blood_test_agent": "service.agents.mock.OstisBloodTestAgent",
        "blood_vitamin_agent": "service.agents.mock.OstisBloodVitaminAgent",
        "blood_micronutrients_agent": "service.agents.mock.OstisBloodMicronutrientsAgent",
        "blood_hormones_test_agent": "service.agents.mock.OstisHormonesBloodTestAgent",
        "diagnosis_agent": "service.agents.ostis.OstisDiagnosisAgent",
    }
    OSTIS_URL = config["DEFAULT"]["ostis_url"]
