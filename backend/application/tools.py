from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from uuid import uuid4
import random
from datetime import datetime, timedelta
from protonmail import ProtonMail


reserved_words = ["app", "home",
                  "terms", "admin", "user", "users", "all"]


def token_tool():
    return URLSafeTimedSerializer(
        current_app.config["SECRET_KEY"],
        current_app.config["SECURITY_PASSWORD_SALT"]
    )


def token_to_user(cur):
    if (
        "Authorization" not in request.headers or
        not request.headers["Authorization"]
    ):
        return None

    token = request.headers["Authorization"]
    try:
        token = token_tool().loads(token)
    except Exception:
        return None

    cur.execute("""
        SELECT * FROM "user" WHERE key = %s AND status != 'deleted';
    """, (token,))
    user = cur.fetchone()
    return user


def generate_code(cur, key, email, _from, clear=True):
    if clear:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (key,))

    code = f"{random.randint(100000, 999999)}"

    cur.execute("""
        INSERT INTO code (key, date, user_key, code, email)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        uuid4().hex,
        datetime.now(),
        key,
        code,
        email
    ))

    return code


def check_code(cur, key, email, n="code"):
    error = None
    if n not in request.json or not request.json[n]:
        error = "this field is required"
    elif len(request.json[n]) != 6:
        error = "invalid code"

    cur.execute("""
        SELECT *
        FROM code
        WHERE
            user_key = %s
            AND code = %s
            AND email = %s;
    """, (
        key,
        request.json[n],
        email
    ))
    code = cur.fetchone()

    if not code:
        error = "invalid code"
    elif datetime.now() - code["date"] > timedelta(minutes=15):
        cur.execute("""
            DELETE FROM code WHERE user_key = %s
        ;""", (key,))
        error = "invalid code"

    return error


def send_mail(to, subject, body):
    if current_app.config["DEBUG"]:
        print(body)
    else:
        proton = ProtonMail()
        proton.login(os.environ["MAIL_USERNAME"], os.environ["MAIL_PASSWORD"])

        proton.send_message(
            proton.create_message(
                recipients=[to],
                subject=subject,
                body=body,
            )
        )


def user_schema(a):
    del a["password"]
    a["photo"] = (
        f"{request.host_url}photo/{a['photo']}"
        if a["photo"] else None
    )
    return a


def org_schema(a):
    if "logo" in a and a["logo"]:
        a["logo"] = f"{request.host_url}photo/{a['logo']}"
    if "icon" in a and a["icon"]:
        a["icon"] = f"{request.host_url}photo/{a['icon']}"
    return a
