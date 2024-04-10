from flask import Flask, render_template_string, render_template, request, redirect, flash, get_flashed_messages
from flask_classful import FlaskView, route
from lib.flask_helpers import admin_level_required
import settings

app = settings.app()
db = settings.db()

class AdminView(FlaskView):
    route_base = '/admin'

    @admin_level_required(7)
    def get(self):

        page_data = {
            'title': 'Admin Page',
            'page_title': 'Sample app admin page'
        }

        return render_template('home.html', page_data=page_data)
