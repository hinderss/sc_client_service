from typing import Required
from marshmallow import Schema, fields


class AuthSchema(Schema):
    username = fields.Str(
        required=True, error_messages={"required": "Username is required."}
    )
    password = fields.Str(
        required=True, error_messages={"required": "Password is required."}
    )


class QuerySchema(Schema):
    query = fields.Str(
        required=True, error_messages={"required": "Search query is required."}
    )
    language = fields.Str(required=False, default="rus")


class BloodSchema(Schema):
    wbc = fields.Float(required=True)
    rbc = fields.Float(required=True)
    platelets = fields.Float(required=True)


class BloodAnalysisSchema(Schema):
    vitamin_e = fields.Float(required=True)
    vitamin_d = fields.Float(required=True)
    vitamin_k = fields.Float(required=True)
    vitamin_c = fields.Float(required=True)
    vitamin_b1 = fields.Float(required=True)
    vitamin_b2 = fields.Float(required=True)
    vitamin_b9 = fields.Float(required=True)
    vitamin_b12 = fields.Float(required=True)
    vitamin_a = fields.Float(required=True)
    vitamin_b6 = fields.Float(required=True)

class BloodMicronutrientsSchema(Schema):
    ca_val = fields.Float(required=True)
    mg_val = fields.Float(required=True)
    fe_val = fields.Float(required=True)

