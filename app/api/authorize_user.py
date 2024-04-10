from flask import make_response, render_template
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

import jwt
import restapi
import settings
import os
from lib.user import User
import re
from api.schemas.authorize_user import *

import logging
import json

app = settings.app()
db = settings.db()
docs = restapi.api_docs()
api = restapi.api_object()
login_manager = settings.login()


@doc(
    description=restapi.render_doc_template('api_docs/authorize_user.html'),
    tags=['Authorization']
)
class AuthorizeUserAPI(MethodResource, Resource):
    uri_path = "/authorize-user"
    @marshal_with(restapi.MessageSchema, description='Invalid user or password', code=400)
    @marshal_with(restapi.MessageSchema, description='This user account is not active', code=301)
    @marshal_with(restapi.MessageSchema, description="Login successful", code=200)
    @use_kwargs(AuthorizeUserSchema, location='json', description='The login credentials for the user')
    def post(self, **kwargs):

        user = User.query.filter_by(
            email=kwargs.get('email')
        ).first()

        if not (user and user.check_password(kwargs.get('password'))):
            error_code = 'AU-400-1'
            error_message = "Invalid user or password"
            status_code = 400
            logging.error(
                '- %s: %s',
                self.__class__.__name__,
                json.dumps({'error_code': error_code, 'message': error_message, 'status_code': status_code, 'data': {'kwargs': kwargs}})
            )
            return restapi.message_response(f"{error_message} ({error_code})", status_code)

        if user.status != 'active':
            error_code = 'AU-301-1'
            error_message = "This user account is inactive"
            status_code = 301
            logging.error(
                '- %s: %s',
                self.__class__.__name__,
                json.dumps({'error_code': error_code, 'message': error_message, 'status_code': status_code, 'data': {'kwargs': kwargs}})
            )
            return restapi.message_response(f"{error_message} ({error_code})", status_code)

        return make_response({
            "response": {
                "token": jwt.encode({
                    "user_id": user.user_id,
                    "admin_level": user.admin_level},
                    os.environ.get("JWT_SECRET"),
                    algorithm="HS256"
                ),
                "user_id": user.user_id,
                "admin_level": user.admin_level
            },
            "app_version": restapi.get_app_version(),
            "status": 200
        }, 200)
