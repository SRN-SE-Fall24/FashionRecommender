from flask import Blueprint, redirect, request, url_for, session, flash, render_template
from flask_login import login_user, login_required, logout_user, current_user
from google_auth_oauthlib.flow import Flow
from werkzeug.security import generate_password_hash, check_password_hash
import os
import pathlib
from google.oauth2 import id_token
from .models import User, Preference
from . import db
from google.auth.transport import requests as google_requests
from . import contracts
import hashlib
import json

GOOGLE_CLIENT_ID = "1086877699482-kv5dvqo6n178o3806o7la513oeqchtmv.apps.googleusercontent.com"

os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

# Initialize blueprint for authentication routes
auth = Blueprint("auth", __name__)

# OAuth2 Configuration
CLIENT_SECRETS_FILE = os.path.join(
    pathlib.Path(__file__).parent.resolve(), "creds.json"
)

flow = Flow.from_client_secrets_file(
    client_secrets_file=CLIENT_SECRETS_FILE,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://127.0.0.1:5000/google-callback",
)


# Google OAuth login route
@auth.route("/google-login")
def google_login():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


# Google OAuth callback route
@auth.route("/google-callback")
def google_callback():
    flow.fetch_token(authorization_response=request.url)
    if not session["state"] == request.args["state"]:
        os.abort(500)

    # Store the credentials in session
    credentials = flow.credentials
    token_request = google_requests.Request()

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    user = User.query.filter_by(email=id_info.get("email")).first()
    if not user:
        user = User(
            email=id_info.get("email"),
            first_name=id_info.get("given_name"),
            last_name=id_info.get("family_name"),
            gender="Unknown",
            phone_number="Unknown",
            age="Unknown",
            city="Unknown",
            password=generate_password_hash("dummy_password"),
        )
        db.session.add(user)
        db.session.commit()

    login_user(user)
    session[contracts.SessionParameters.USERID] = user.get_id()

    if (
        user.gender == "Unknown"
        or user.phone_number == "Unknown"
        or user.age == "Unknown"
        or user.city == "Unknown"
    ):
        return redirect(url_for("auth.profile_update", userid=user.id))

    return render_template("home.html", user=current_user)


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if hashlib.sha256(password.encode()).hexdigest() == user.password:
                flash("Logged in successfully!", category="success")
                session[contracts.SessionParameters.USERID] = user.get_id()
                login_user(user, remember=True)
                return render_template("home.html", user=user)
            else:
                flash("Incorrect password, try again.", category="error")
        else:
            flash("Email does not exist.", category="error")

    return render_template("login.html", user=current_user)


# Sign up route
@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        last_name = request.form.get("lastName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        gender = request.form.get("gender")
        phone_number = request.form.get("phoneNumber")
        city = request.form.get("city")
        age = request.form.get("age")

        user = User.query.filter_by(email=email).first()
        if user:
            flash("Email already exists.", category="error")
        elif len(email) < 4:
            flash("Email must be greater than 3 characters.", category="error")
        elif len(first_name) < 2:
            flash("First name must be greater than 1 character.", category="error")
        elif password1 != password2:
            flash("Passwords don't match.", category="error")
        elif len(password1) < 7:
            flash("Password must be at least 7 characters.", category="error")
        elif int(age) < 18 or int(age) > 90:
            flash("Please enter a valid age", category="error")
        else:
            new_user = User(
                email=email,
                first_name=first_name,
                last_name=last_name,
                gender=gender,
                city=city,
                age=age,
                phone_number=phone_number,
                password=hashlib.sha256(password1.encode()).hexdigest(),
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("Account created!", category="success")
            return render_template("home.html", user=new_user)

    return render_template("sign_up.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    session.pop(contracts.SessionParameters.USERID, None)
    return redirect(url_for("auth.login"))


@auth.route("/profile-update", methods=["GET", "POST"])
def profile_update():
    # For the post request.
    if request.method == "POST":
        phone_number = request.form.get("phoneNumber")
        city = request.form.get("city")
        age = request.form.get("age")
        userid = request.form.get("userid")

        user = User.query.filter_by(id=int(userid)).first()

        if int(age) < 18 or int(age) > 90:
            flash("Please enter a valid age", category="error")
        else:
            user.age = age
            user.city = city
            user.phone_number = phone_number
            db.session.commit()
            flash("Account updated!", category="success")
            return render_template("home.html", user=user)

    # For get request.
    preferenceObject = Preference.query.filter_by(userid=int(current_user.id)).first()
    if preferenceObject:
        try:
            prefData = json.loads(preferenceObject.preferences)
        except json.JSONDecodeError:
            prefData = {}
    else:
        prefData = {}

    return render_template("profile.html", user=current_user, prefData=prefData)
