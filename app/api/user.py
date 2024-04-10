from flask import request, make_response
from flask_restful import Resource, Api
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource

import settings
import restapi
import json
import logging
import os

from datetime import datetime

from lib.user import User
from api.schemas.user import *

app = settings.app()
db = settings.db()
docs = restapi.api_docs()
api = restapi.api_object()
login_manager = settings.login()


@doc(
    description=restapi.render_doc_template('api_docs/user.html'),
    tags=['User'],
    params={
        "authorization": {
            "description": "User auth token",
            "in": "header",
            "type": "string",
            "required": True,
            "name": "Authorization"
        },
        "user_id": {
            "description": "ID of the user to query",
            "in": "path",
            "type": "string",
            "required": True
        }
    }
)
class UserQueryAPI(MethodResource, Resource):
    uri_path = '/user/<user_id>'
    @marshal_with(UserObject, description="User details", code=200)
    @marshal_with(restapi.MessageSchema, description="Access denied", code=403)
    @marshal_with(restapi.MessageSchema, description="User not found", code=404)
    def get(self, user_id):
        token = User.api_user(request.headers.get('Authorization'))

        if token['status'] != 200:
            logging.error(
                '- %s: %s',
                'UserQueryAPI',
                json.dumps({
                    'error_code': 'U-403-1',
                    'data': {
                        'token': request.headers.get('Authorization'),
                        'kwargs': {
                            'user_id': user_id
                        }
                    }
                })
            )
            return restapi.message_response("Access denied (U-403-1)", 403)

        user = User.query.filter_by(
            user_id=user_id
        ).first()

        if not user:
            logging.error(
                '- %s: %s',
                'UserQueryAPI',
                json.dumps({
                    'error_code': 'U-404-1',
                    'data': {
                        'token': request.headers.get('Authorization'),
                        'kwargs': {
                            'user_id': user_id
                        },
                        'user': token['user'].json()
                    }
                })
            )
            return restapi.message_response("User not found (U-404-1)", 404)

        resp = {
            'user': user.to_dict()
        }

        return make_response({
            "response": resp,
            "app_version": restapi.get_app_version(),
            "status": 200
        }, 200)
