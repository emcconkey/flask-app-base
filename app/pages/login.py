from flask import Flask, render_template_string, render_template, request, redirect, flash
from flask_classful import FlaskView, route
from flask_login import current_user, login_user
import settings
from lib.user import User

app = settings.app()
db = settings.db()


class LoginView(FlaskView):
    route_base = '/login'

    def get(self):
        return render_template('login.html', page_data={'page_title': 'Login'})


    def post(self):
        user = User.query.filter_by(
            email=request.form.get('username')
        ).first()

        if not (user and user.check_password(request.form.get('password'))):
            flash("The username or password provided do not match any records in the system.", 'error')
            return redirect('/login')

        if user.status != 'active':
            flash("Your user account has been disabled, please contact customer support.", 'error')
            return redirect('/login')

        login_user(user)
        return redirect('/')

