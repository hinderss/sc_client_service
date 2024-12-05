from flask import Blueprint, request, jsonify

from .schemas.input import (
    AuthSchema as AuthInputSchema,
    BloodAnalysisSchema,
    BloodMicronutrientsSchema,
    QuerySchema,
    BloodSchema, BloodHormonesSchema,
)
from .schemas.output import AuthSchema as AuthOutputSchema, BaseMessageSchema, ListMessageSchema
from .schemas.output import RegSchema as RegOutputSchema
from .services import (
    auth_agent,
    blood_vitamin_agent,
    blood_micronutrients_agent,
    reg_agent,
    navigation_agent,
    recommendation_agent,
    blood_test_agent, blood_hormones_test_agent,
)

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
    language = data.get("language")

    output = navigation_agent(query, language)

    return jsonify(BaseMessageSchema().dump(output)), 200


@main.route("/rec", methods=["POST"])
def rec():
    data = QuerySchema().load(request.get_json())

    query = data["query"]

    output = recommendation_agent(query)

    return jsonify(BaseMessageSchema().dump(output)), 200


@main.route("/blood", methods=["POST"])
def blood():
    data = BloodSchema().load(request.get_json())

    wbc = data["wbc"]
    rbc = data["rbc"]
    platelets = data["platelets"]

    output = blood_test_agent(wbc, rbc, platelets)

    return jsonify(ListMessageSchema().dump(output)), 200


@main.route("/blood_vitamin", methods=["POST"])
def blood_analysis():
    data = BloodAnalysisSchema().load(request.get_json())

    vitamin_e = data["vitamin_e"]
    vitamin_d = data["vitamin_d"]
    vitamin_k = data["vitamin_k"]
    vitamin_c = data["vitamin_c"]
    vitamin_b1 = data["vitamin_b1"]
    vitamin_b2 = data["vitamin_b2"]
    vitamin_b9 = data["vitamin_b9"]
    vitamin_b12 = data["vitamin_b12"]
    vitamin_a = data["vitamin_a"]
    vitamin_b6 = data["vitamin_b6"]

    output = blood_vitamin_agent(
        vitamin_e,
        vitamin_d,
        vitamin_k,
        vitamin_c,
        vitamin_b1,
        vitamin_b2,
        vitamin_b9,
        vitamin_b12,
        vitamin_a,
        vitamin_b6,
    )

    return jsonify(ListMessageSchema().dump(output)), 200


@main.route("/blood_micronutrients", methods=["POST"])
def blood_micronutrients():
    data = BloodMicronutrientsSchema().load(request.get_json())

    ca_val = data["ca"]
    mg_val = data["mg"]
    fe_val = data["fe"]

    output = blood_micronutrients_agent(
        ca_val,
        mg_val,
        fe_val,
    )

    return jsonify(ListMessageSchema().dump(output)), 200


@main.route("/blood_hormones", methods=["POST"])
def blood_hormones():
    data = BloodHormonesSchema().load(request.get_json())

    tsh_val = data["tsh"]
    fsh_val = data["fsh"]
    lh_val = data["lh"]

    output = blood_hormones_test_agent(
        tsh_val,
        fsh_val,
        lh_val,
    )

    return jsonify(ListMessageSchema().dump(output)), 200
