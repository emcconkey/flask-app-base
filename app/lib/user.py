import settings
db = settings.db()
from flask_login import UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re, jwt, os, json
from sqlalchemy import or_

from lib.reset_token import ResetToken


class User(UserMixin, db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), index=True)
    password = db.Column(db.String(255))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    admin_level = db.Column(db.Integer)
    phone = db.Column(db.String(255))
    status = db.Column(db.String(255))
    account_created = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User #{self.user_id}: {self.email}>'

    def name(self):
        return f"{self.first_name} {self.last_name}"

    def get_id(self):
        return self.user_id

    def get_admin_level(self):
        return self.admin_level

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def delete_account(self):
        ResetToken.query.filter_by(user_id=self.user_id).delete()
        User.query.filter_by(user_id=self.user_id).delete()
        db.session.commit()

    def delete_reset_tokens(self):
        ResetToken.query.filter_by(user_id=self.user_id).delete()
        db.session.commit()

    def to_dict(self, internal=False):
        output = {
            'user_id': self.user_id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'phone': self.phone,
            'status': self.status,
            'account_created': self.account_created
        }

        if internal:
            output['admin_level'] = self.admin_level

        return output

    def json(self):
        return {
            'user_id': self.user_id,
            'admin_level': self.admin_level,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'phone': self.phone,
            'status': self.status,
        }

    @staticmethod
    def query_users():
        return User.query.filter(
            or_(
                User.email == None  # Needed as the first filter removed emails = none
            )
        )

    @staticmethod
    def strip_phone_number(phone_number):
        return re.sub("[^0-9a-zA-Z:,]", "", phone_number)

    @staticmethod
    def api_user(token=None):
        if current_user.is_authenticated:
            return {
                "user": current_user,
                "status": 200
            }
        if token:
            try:
                token = token.replace('Bearer ', '', 1)
                token = jwt.decode(token, os.environ.get('JWT_SECRET'), algorithms="HS256")
            except:
                return {
                    "response": "Unable to parse token",
                    "status": 500
                }

            user = User.query.filter_by(user_id=token["user_id"]).first()
            if user:
                return {
                    "user": user,
                    "status": 200
                }
        return {
            "response": "Invalid token",
            "status": 404
        }

    @staticmethod
    def valid_email(email):
        return re.search('^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$', email)

    @staticmethod
    def valid_phone(phone_number):
        return re.fullmatch('(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})', phone_number)

    @staticmethod
    def get_admin_level_map():
        return {
            2: "User",
            5: "Manager",
            7: "Admin"
        }

    @staticmethod
    def get_manager_level_map():
        return {
            2: "User",
            5: "Manager"
        }

    @staticmethod
    def get_status_map():
        return {
            "active": "Active",
            "inactive": "Inactive"
        }