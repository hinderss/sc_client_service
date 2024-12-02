from marshmallow import Schema, fields


class AuthSchema(Schema):
    username = fields.Str(required=True, error_messages={"required": "Username is required."})
    password = fields.Str(required=True, error_messages={"required": "Password is required."})


class QuerySchema(Schema):
    query = fields.Str(required=True, error_messages={"required": "Search query is required."})
    language = fields.Str(required=False, default="rus")


class BloodSchema(Schema):
    wbc = fields.Float(required=True)
    rbc = fields.Float(required=True)
    platelets = fields.Float(required=True)
