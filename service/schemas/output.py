from marshmallow import Schema, fields, validate

from service.agents.abstract.auth_agent import AuthStatus, RegStatus


class BaseMessageSchema(Schema):
    message = fields.Str(required=True)


class ListMessageSchema(Schema):
    message = fields.List(fields.Str, required=True, allow_none=True)


class AuthSchema(Schema):
    status = fields.String(required=True, validate=validate.OneOf([e for e in AuthStatus]))
    message = fields.Str(required=False)


class RegSchema(Schema):
    status = fields.String(required=True, validate=validate.OneOf([e for e in RegStatus]))
    message = fields.Str(required=False)
