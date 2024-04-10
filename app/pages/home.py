from flask import Flask, render_template_string, render_template, request, redirect, flash, get_flashed_messages
from flask_classful import FlaskView, route
from flask_login import current_user
import settings

app = settings.app()
db = settings.db()


class HomeView(FlaskView):
    route_base = '/'

    def get(self):
        if not current_user.is_authenticated:
            return redirect('/login')

        page_data = {
            'title': 'Dashboard',
            'page_title': 'Welcome to sample app'
        }

        return render_template('home.html', page_data=page_data)


