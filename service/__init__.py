from flask import Flask

from .agent_factory import load_agents
from .views import main


def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")

    app.register_blueprint(main)

    app.config['agents'] = load_agents()

    return app
