import configparser


class Config:
    config = configparser.ConfigParser()
    config.read('config.ini')

    AGENTS_TO_LOAD = {
        "auth_agent": "service.agents.mock.OstisAuthAgent",
    }
    OSTIS_URL = "ws://localhost:8090/ws_json"
    PORTAL_URL = "http://localhost:1025"

