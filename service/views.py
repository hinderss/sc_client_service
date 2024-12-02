from flask import Blueprint, request, jsonify

from .schemas.input import AuthSchema as AuthInputSchema, QuerySchema, BloodSchema
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
    data = QuerySchema().load(request.get_json())

    query = data["query"]
    language = data["language"]

    output = navigation_agent(query, language)

    return jsonify(output), 200


@main.route("/rec", methods=["POST"])
def rec():
    data = QuerySchema().load(request.get_json())

    query = data["query"]

    output = recommendation_agent(query)

    return jsonify(output), 200


@main.route("/blood", methods=["POST"])
def blood():
    data = BloodSchema().load(request.get_json())

    wbc = data["wbc"]
    rbc = data["rbc"]
    platelets = data["platelets"]

    output = blood_test_agent(wbc, rbc, platelets)

    return jsonify(output), 200
