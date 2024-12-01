import configparser


class Config:
    config = configparser.ConfigParser()
    config.read('config.ini')

    AGENTS_TO_LOAD = {
        "auth_agent": "service.agents.ostis.OstisAuthAgent",
        "navigation_agent": "service.agents.ostis.OstisNavigationAgent",
        "recommendation_agent": "service.agents.ostis.OstisRecommendationAgent",
        "blood_test_agent": "service.agents.ostis.OstisBloodTestAgent"
    }
    OSTIS_URL = "ws://localhost:8090/ws_json"
    PORTAL_URL = "http://localhost:1025"

