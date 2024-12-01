from flask import Blueprint, request

from .services import auth_agent, reg_agent, navigation_agent, recommendation_agent, blood_test_agent

main = Blueprint("main", __name__)


@main.route("/auth", methods=["POST"])
def auth():
    username = request.form.get("username")
    password = request.form.get("password")

    if username and password:
        output = auth_agent(username, password)
    else:
        return "Username and password are required", 400

    return output, 200


@main.route("/reg", methods=["POST"])
def reg():
    username = request.form.get("username")
    password = request.form.get("password")

    if not (username and password):
        return "Username and password are required", 400

    reg_agent(username, password)

    return "Registration successful", 200


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
