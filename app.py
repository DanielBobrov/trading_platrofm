import datetime
import os
import sqlite3

from flask import Flask, session, render_template, redirect, request, g, abort

from config import Config
from database import User, Application, DataBase

app = Flask(__name__)
app.config.from_object(Config)
app.config.update(dict(DATABASE=os.path.join(app.root_path, 'database.db')))
app.permanent_session_lifetime = datetime.timedelta(days=5)


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


def check_login(form):
    member_login = form.get("login")
    member_password = request.form.get("password")
    return DataBase().check_password(member_login, member_password)


@app.route("/", methods=["GET"])
def main():
    db = DataBase()
    apps = [Application(app=i) for i in db.get_applications()]
    user = session.get("user_login", None)
    user = User(login=user) if user else user
    return render_template("main.html", apps=apps, user=user, login_error=request.args.get("login_error", ""))


@app.route("/login/", methods=["POST"])
def login():
    logged = check_login(request.form)
    if logged:
        session["user_login"] = request.form.get("login")
    fr = request.form.get("from", None)
    return redirect(f"/{fr + '/' if fr else ''}{'?login_error=True' if not logged else ''}")


@app.route("/logout/", methods=["GET", "POST"])
def logout():
    session.clear()
    fr = request.args.get("from", None)
    return redirect(f"/{fr + '/' if fr else ''}")


@app.route("/end_application/<int:app_id>/<int:responser_id>/", methods=["GET", "POST"])
def end_app(app_id, responser_id):
    app = Application(id=app_id)
    app.end(responser_id)
    fr = request.args.get("from", None)
    return redirect(f"/{fr + '/' if fr else ''}")


@app.route("/create_application/", methods=["GET", "POST"])
def create_app():
    user = session.get("user_login", None)
    if user is None:
        return abort(404)
    if request.method == "GET":
        return render_template("create_application.html", user=user)
    user = User(login=user)
    price = request.form.get("price", "")
    user.add_app(DataBase().create_application(user.id, price + " р." if price else "Договорная", request.form["title"],
                                               request.form["description"]))
    return redirect("/")


@app.route("/profile/<int:user_id>/", methods=["GET"])
def profile(user_id):
    user = User(id=user_id)
    apps = [Application(id=i) for i in user.apps]
    responses = [Application(id=i) for i in user.responses]
    return render_template("profile.html", user=user, apps=apps, responses=responses, login_error=request.args.get("login_error", ""))


@app.route("/application/<int:app_id>/", methods=["GET"])
def application(app_id):
    app = Application(id=app_id)
    user = session.get("user_login", None)
    user = User(login=user) if user else None
    responses = tuple(app.responses)
    for i in range(len(app.responses)):
        app.responses[i] = User(id=app.responses[i])
    print(app.active)
    return render_template("application.html", app=app, user=user, responses=responses, login_error=request.args.get("login_error", ""), creator=User(id=app.creator_id))


@app.route("/create_response/<int:app_id>/<int:user_id>/", methods=["GET"])
def create_response(app_id, user_id):
    app = Application(id=app_id)
    app.add_response(user_id)
    user = User(id=user_id)
    user.add_response(app_id)
    return redirect(f"/application/{app_id}/")


@app.route("/delete_response/<int:app_id>/<int:user_id>/", methods=["GET"])
def delete_response(app_id, user_id):
    app = Application(id=app_id)
    app.delete_response(user_id)
    user = User(id=user_id)
    user.delete_response(app_id)
    return redirect(f"/application/{app_id}/")


@app.errorhandler(404)
def page_not_found(error):
    return redirect("/")


if __name__ == '__main__':
    app.run(debug=True)
