from marshmallow import Schema, fields


class AuthorizeUserSchema(Schema):
    email = fields.String()
    password = fields.String()


class Token(Schema):
    token = fields.String()
    user_id = fields.Integer()


class TokenSchema(Schema):
    response = fields.Nested(Token)
    status = fields.Integer()
