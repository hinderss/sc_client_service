from flask import Blueprint, request

from .services import auth_agent, reg_agent

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
