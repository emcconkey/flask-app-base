from flask import make_response, request
from flask_restful import Api
from flask_login import current_user
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask_apispec.extension import FlaskApiSpec
import jinja2
import os
import settings
import logging
import json
from lib.user import User

from marshmallow import Schema, fields
from lib.app_version import AppVersion

app = settings.app()
db = settings.db()
api = Api(app)
login_manager = settings.login()


def render_doc_template(template_file):
    # Read the template file into a variable
    with open('templates/' + template_file) as f:
        api_doc_template = f.read()
    # Create a Jinja2 template object
    template = jinja2.Template(api_doc_template)
    return template.render()


spec = APISpec(
    title='Sample app API',
    info=dict(
        description=render_doc_template('api_docs/main.html'),
        version='v1'
    ),
    version='v1',
    plugins=[MarshmallowPlugin()],
    openapi_version='2.0.0'
)
# token_auth = {"type": "apiKey", "name": "Authorization", "in": "header"}
# spec.components.security_scheme("JWT", token_auth)

app.config.update({
    'APISPEC_SPEC': spec,
    'APISPEC_SWAGGER_URL': os.environ.get('API_PATH') + '/api-json/',
    'APISPEC_SWAGGER_UI_URL': os.environ.get('API_PATH') + '/docs/'
})
docs = FlaskApiSpec(app)

if os.environ.get('DEBUG_LOGFILE'):
    # Create a logger for debug messages
    debug_logger = logging.getLogger('debug')
    debug_logger.setLevel(logging.DEBUG)
    debug_handler = logging.FileHandler(os.environ.get('DEBUG_LOGFILE'))
    debug_handler.setLevel(logging.DEBUG)
    debug_formatter = logging.Formatter('[%(asctime)s] %(module)s %(message)s')
    debug_handler.setFormatter(debug_formatter)
    debug_logger.addHandler(debug_handler)
else:
    debug_logger = False


# Change swagger theme
# /flask-apispec/static/swagger-ui.css
@app.route('/flask-apispec/static/swagger-ui.css')
def send_css():
    return app.send_static_file('swagger/theme-flattop.css')


def message_response(message, status_code):
    return make_response(
        {
            "message": message,
            "app_version": AppVersion.get_app_version(),
            "status": status_code
        },
        status_code
    )


def redirect_message_response(message, url, redirect_type, status_code, specifier=""):
    return make_response(
        {
            "message": message,
            "redirect": {
                "url": url,
                "specifier": specifier,
                "type": redirect_type
            },
            "app_version": AppVersion.get_app_version(),
            "status": status_code
        },
        status_code
    )


def get_app_version():
    return AppVersion.get_app_version()


class AppVersionSchema(Schema):
    android = fields.String()
    ios = fields.String()


class RedirectSchema(Schema):
    url = fields.String()
    specifier = fields.String()
    type = fields.String()


class MessageSchema(Schema):
    message = fields.String()
    app_version = fields.Nested(AppVersionSchema)
    status = fields.Integer()


class RedirectMessageSchema(Schema):
    message = fields.String()
    redirect = fields.Nested(RedirectSchema)
    app_version = fields.Nested(AppVersionSchema)
    status = fields.Integer()


def api_object():
    return api


def api_docs():
    return docs


@app.before_request
def log_requests():
    if not debug_logger:
        return
    token = request.headers.get('Authorization')
    if not token:
        return
    user = User.api_user(token)
    if not user or 'response' in user:
        user_json = {'user': {'user_id': 0, 'email': 'Unknown'}}
    else:
        user_json = user['user'].json()
    debug_logger.debug(
        '- %s: %s',
        'Request',
        json.dumps({
            'method': request.method,
            'url': request.url,
            'token': request.headers.get('Authorization'),
            'user': user_json,
            'data': str(request.data),
            'headers': str(request.headers)
        })
    )


@app.before_request
def apidocs_check_auth():
    if not os.environ.get('APIDOCS_REQUIRE_AUTH'):
        return

    apidocpath = app.config['APISPEC_SWAGGER_UI_URL']
    apijsonpath = app.config['APISPEC_SWAGGER_URL']
    # See if the request path starts with the API path
    if request.path[0:len(apidocpath)] != apidocpath and request.path[0:len(apijsonpath)] != apijsonpath:
        return

    if not current_user.is_authenticated or current_user.admin_level < int(os.environ.get('APIDOCS_REQUIRE_AUTH_LEVEL')):
        return make_response(
            {
                "message": "You do not have access to this resource",
                "status": 401
            },
            401
        )


@app.after_request
def add_header(response):
    if os.environ.get('FLASK_DEBUG') == "1":
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Authorization, Origin, Accept, Version'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    elif os.environ.get('RUN_MODE') == 'dev':
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'X-Requested-With, Content-Type, Authorization, Origin, Accept, Version'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    else:
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, Version'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, PATCH, DELETE'
    return response
