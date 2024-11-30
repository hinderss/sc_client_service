from flask import Blueprint, request, jsonify

from .schemas.input import AuthSchema as AuthInputSchema
from .schemas.output import AuthSchema as AuthOutputSchema
from .schemas.output import RegSchema as RegOutputSchema
from .services import auth_agent, reg_agent, navigation_agent, recommendation_agent, blood_test_agent

main = Blueprint("main", __name__)


@main.route("/auth", methods=["POST"])
def auth():
    data = AuthInputSchema().load(request.get_json())

    username = data["username"]
    password = data["password"]

    output = auth_agent(username, password)
    return jsonify(AuthOutputSchema().dump(output)), 200


@main.route("/reg", methods=["POST"])
def reg():
    data = AuthInputSchema().load(request.get_json())

    username = data["username"]
    password = data["password"]

    output = reg_agent(username, password)

    return jsonify(RegOutputSchema().dump(output)), 200


@main.route("/nav", methods=["POST"])
def nav():
    node_name = request.form.get("node_name")
    node_lang = request.form.get("node_lang")

    if not (node_name and node_lang):
        return "Node name is required", 400

    navigation_agent(node_name, node_lang)

    return "Navigation successful", 200


@main.route("/rec", methods=["POST"])
def nav():
    node_name = request.form.get("node_name")

    if not node_name:
        return "Node name is required", 400

    recommendation_agent(node_name)

    return "Recommendation successful", 200
