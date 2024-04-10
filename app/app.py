import glob
from runpy import run_path
from flask import request, redirect, render_template
from flask_classful import FlaskView
from flask_restful import Resource
import settings
from lib.user import User
from flask_login import current_user
import os
from datetime import datetime
from datetime import timedelta
import restapi

import datetime


app = settings.app()
migrate = settings.migrate()
db = settings.db()
login_manager = settings.login()
docs = restapi.api_docs()
api = restapi.api_object()

# Load and register all the pages and API endpoints
modules = glob.glob('pages/*.py')
modules += glob.glob('api/*.py')

for m in modules:
    res = run_path(m)
    for r in res:
        # Check if this is a FlaskView class
        # Don't do any error checking, we want the app to fail to start if one of the pages is broken
        if isinstance(res[r], type) and issubclass(res[r], FlaskView) and res[r] != FlaskView:
            print(f"Registering page {r}")
            res[r].register(app)

        if isinstance(res[r], type) and issubclass(res[r], Resource) and res[r] != Resource:
            print(f"Registering API {r}")
            api.add_resource(res[r], os.environ.get('API_PATH') + res[r].uri_path)
            docs.register(res[r])

# Done registering pages/endpoints

@app.before_request
def before_request():
    # Force https redirect if we're behind a proxy
    e = request.environ
    if 'HTTP_X_FORWARDED_PROTO' in e:
        if e['HTTP_X_FORWARDED_PROTO'] == 'http':
            return redirect(f"https://{request.host}{request.path}", code=301)

    if request.path[0:8] == '/static/':
        return


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.errorhandler(404)
def page_error_404(e):
    return render_template('404.html', page_data={'page_title': 'Page Not Found'}), 404

@app.errorhandler(401)
def page_error_401(e):
    return render_template('401.html', page_data={'page_title': 'Access Denied'}), 401


@app.context_processor
def add_user():
    return dict(
        current_user=current_user.to_dict(internal=True) if
            current_user.is_authenticated
        else
            {
                'admin_level': 0
            }
    )


@app.template_filter()
def format_datetime(value):
    # TODO: fix this cheesy hack
    dt = value - timedelta(hours=7)
    return datetime.datetime.strftime(dt, '%m/%d/%y %I:%M %p')


@app.template_filter()
def format_date(value):
    return datetime.datetime.strftime(value, '%m/%d/%y')

@app.template_filter()
def process_image_data(data):
    return (data.split(b',')[-1]).decode('ascii')


@app.template_filter()
def bitwise_and(x, y):
    return x & y


@app.template_filter()
def bitshift_right(value, shift):
    return value >> shift


@app.template_filter()
def bitshift_left(value, shift):
    print(f"[{value}] [{shift}]")
    return value << shift


def getenv(key):
    return os.environ.get(key)



def run_tasks():
    print("Running tasks")
    if os.environ.get('SAMPLE_TASK'):
        print("Running sample task")
    exit(0)


app.jinja_env.globals.update(getenv=getenv)

if os.environ.get('RUN_TASKS'):
    run_tasks()

if __name__ == '__main__':
    app.run(threaded=False)
