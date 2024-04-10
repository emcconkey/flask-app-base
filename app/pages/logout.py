from flask import Flask, render_template_string, render_template, request, redirect, flash
from flask_classful import FlaskView, route
from flask_login import current_user, logout_user
import settings

app = settings.app()
db = settings.db()


class LogoutView(FlaskView):
    route_base = '/logout'

    def get(self):
        if current_user.is_authenticated:
            logout_user()
        return redirect('/login')

