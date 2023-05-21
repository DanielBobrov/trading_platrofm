import datetime
import json
import os
import sqlite3

import requests
from flask import Flask, session, render_template, redirect, request, g, url_for, abort

from config import Config
from database import DataBase

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))
app.permanent_session_lifetime = datetime.timedelta(days=15)


def connect_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
        return g.link_db


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "link_db"):
        g.link_db.close()


@app.route("/", methods=["GET", "POST"])
def main():
    db = DataBase()
    """    if request.method == "POST":
        form = request.form
        match form.get("type"):
            case "create_application":
                price = form.get("price")
                db.create_application(
                    form.get("creator_id"),
                    price + " р." if price else "Договорная",
                    form.get("title"),
                    form.get("description"),
                )
    """
    member = session.get("member")
    if member is not None:
        member = {key: member[key] for key in member.keys()}
    applications = db.get_applications()
    return render_template(
        "main.html",
        applications=applications,
        member=member,
    )


def collect_users_applications(id_customer):
    db = DataBase()
    applications = db.get_applications()
    users_aplications = []
    for app in applications:
        if app['creator_id'] == id_customer:
            users_aplications.append(app)
    return users_aplications


def collect_users_response(id_customer):
    db = DataBase()
    applications = db.get_applications()
    users_responses = []
    for app in applications:
        if id_customer in list(map(int, app['responses'].split())):
            users_responses.append(app)
    return users_responses


def alien_profile(id_customer):
    if id_customer == session.get("member"):
        return redirect("/profile/")
    db = DataBase()
    member = db.get_member(f"id={id_customer}")
    applications = collect_users_applications(id_customer)
    response = collect_users_response(id_customer)
    return render_template("alien_profile-page.html", member=member, applications=applications, response=response)


def my_profile():
    db = DataBase()
    member = db.get_member(f"id = {session.get('member')['id']}")
    if request.method == "POST":
        form = request.form
        if 'delete' in form.get('profile'):
            deletes_id = form.get('delete_id')
            db.delete_application(deletes_id)
        elif "text-info" in form.get("profile"):
            db.update_member(member["id"], f"name = '{form.get('name')}'")
            db.update_member(member["id"], f"surname = '{form.get('surname')}'")
            db.update_member(member["id"], f"email = '{form.get('email')}'")
            db.update_member(member["id"], f"telephone_number ='{form.get('phone-number')}'")
            db.update_member(member["id"], f"password = '{form.get('password')}'")
            db.update_member(member["id"], f"description = '{form.get('about-me')}'")
            member = db.get_member(f"id = {session.get('member')['id']}")
    applications = collect_users_applications(member['id'])
    response = collect_users_response(member['id'])
    return render_template(
        "profile.html",
        member=member,
        applications=applications,
        response=response,
    )


@app.route("/profile/<int:id_customer>", methods=["GET", "POST"])
def profile(id_customer):
    if id_customer != session.get("member"):
        return alien_profile(id_customer)
    else:
        return my_profile()



def check_form(form):
    for k, v in form.items():
        if not (v):
            return False
    return True


@app.route("/login/", methods=["POST"])
def login():
    form = request.form
    if not (check_form(form)):
        return abort(403)
    try:  # если что то не ввели
        user_login = form.get("login")
        user_password = form.get("password")
    except Exception as e:
        print(f"[ERROR IN LOGIN]\n {form}")
        return abort(403)

    if form.get('lr') == 'register':  # если регистрация, lt-login-register
        try:
            user_name, user_surname, user_login, user_email, user_password = form.get("name"), form.get(
                "surname"), form.get("login"), form.get("email"), form.get("password")
        except Exception as e:
            print(f"[ERROR IN LOGIN]\n {form}")
            return abort(403)
        DataBase().create_member(user_name, user_surname, user_email, "", "", user_login, user_password)
    member = DataBase().get_member(f"login = '{user_login}'")
    print('[INPUTS(login, password)] ---', user_login, user_password)
    if member is not None and member["password"] == user_password:
        member = {key: member[key] for key in member.keys()}
        session["member"] = member
        return redirect("/")
    else:
        print('[НЕ ВЕРНЫЙ ПАРОЛЬ]')
        return redirect("/")  # abort(403)


@app.route("/logout/")
def logout():
    session.clear()
    return redirect("/")


@app.route("/create_application/", methods=["GET", "POST"])
def create_application():
    db = DataBase()
    if request.method == "POST":
        form = request.form
        match form.get("type"):
            case "create_application":
                price = form.get("price")
                db.create_application(
                    form.get("creator_id"),
                    price + " р." if price else "Договорная",
                    form.get("title"),
                    form.get("description"),
                )
        return redirect('/')
    return render_template(
        "create_application.html",
        member=session["member"],
    )


@app.route("/end_application/<int:app_id>/<int:responser_id>")
def end_application(app_id: int, responser_id: int):
    db = DataBase()
    db.end_application(app_id, responser_id)
    return redirect(f"/application/{app_id}/")


@app.route("/application/<int:app_id>/edit/", methods=["GET", "POST"])
def edit_application(app_id: int):
    db = DataBase()
    if request.method == "POST":
        title = request.form.get("title")
        price = request.form.get("price")
        description = request.form.get("description")
        db.update_application(app_id, f"title = '{title}'")
        db.update_application(app_id, f"price = '{price}'")
        db.update_application(app_id, f"description = '{description}'")
        return redirect(f"application/{app_id}/")
    application = db.get_application(app_id)
    if session["member"]["id"] != application["creator_id"]:
        return abort(403)
    if application is not None:
        application = {key: application[key] for key in application.keys()}
        application["creator_id"] = str(application["creator_id"])
        if application["responses"] is None:
            application["responses"] = ""
        responses = application["responses"]
        responses = [db.get_member(f"id = {i}") for i in responses.split()]
    member = session.get("member")
    if member is not None:
        member = {key: member[key] for key in member.keys()}
        member["id"] = str(member["id"])
    return render_template(
        "edit_application.html",
        member=member,
        app=application,
        responses=responses,
        len=len,
        creator=member,
    )


@app.route("/application/<int:app_id>/")
def get_application(app_id: int):
    db = DataBase()
    application = db.get_application(app_id)
    if application is not None:
        application = {key: application[key] for key in application.keys()}
        application["creator_id"] = str(application["creator_id"])
        if application["responses"] is None:
            application["responses"] = ""
        responses = application["responses"]
        responses = [db.get_member(f"id = {i}") for i in responses.split()]
    member = session.get("member")
    if member is not None:
        member = {key: member[key] for key in member.keys()}
        member["id"] = str(member["id"])
    creator = db.get_member(f"id = {application['creator_id']}")
    return render_template(
        "application.html",
        member=member,
        app=application,
        responses=responses,
        len=len,
        creator=creator,
    )


@app.route("/response/<int:app_id>/<int:responser_id>")
def response_application(app_id: int, responser_id: int):
    db = DataBase()
    db.add_responser(app_id, responser_id)
    return redirect(f"/application/{app_id}")


@app.route("/test")
def test():
    return render_template("test.html")


@app.route("/t")
def t():
    return render_template("profile.html")


@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
