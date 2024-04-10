from marshmallow import Schema, fields


class UserObject(Schema):
    user_id = fields.Integer(required=False)
    email = fields.String(required=False)
    first_name = fields.String(required=False)
    last_name = fields.String(required=False)
    phone = fields.String(required=False)
    status = fields.String(required=False)
    account_created = fields.DateTime(required=False)

