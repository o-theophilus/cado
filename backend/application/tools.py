from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import os
from uuid import uuid4
import random
from datetime import datetime, timedelta
import smtplib
import ssl
from email.mime.text import MIMEText


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


def generate_code(cur, key, email, clear=True):
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
    if (
        not request.json
        or n not in request.json
        or not request.json[n]
    ):
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
        request.json[n] if request.json and n in request.json else None,
        email
    ))
    code = cur.fetchone()

    if not code:
        error = "invalid code"
    elif datetime.now() - code["date"] > timedelta(minutes=15):
        cur.execute("DELETE FROM code WHERE user_key = %s;", (key,))
        error = "invalid code"

    return error


def send_mail(to, subject, body):
    print(f"Sending email to {to} with subject '{subject}'")

    # if current_app.config["DEBUG"]:
    #     print(body)
    # else:
    msg = MIMEText(body, "html")
    msg['Subject'] = subject
    msg['From'] = os.environ["MAIL_USERNAME"]
    msg['To'] = to

    context = ssl.create_default_context()

    try:
        with smtplib.SMTP("workplace.truehost.cloud", 587) as server:
            server.starttls(context=context)
            server.login(os.environ["MAIL_USERNAME"],
                         os.environ["MAIL_PASSWORD"])
            server.sendmail(os.environ["MAIL_USERNAME"], [to], msg.as_string())

        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {e}")


def user_schema(a):
    del a["password"]
    a["photo"] = (
        f"{request.host_url}photo/{a['photo']}"
        if a["photo"] else None
    )
    return a


def card_schema(a):
    a["photo"] = (
        f"{request.host_url}photo/{a['photo']}"
        if a["photo"] else None
    )

    if "org" in a:
        a["org"]["photo"] = (
            f"{request.host_url}photo/{a["org"]['photo']}"
            if a["org"]["photo"] else None
        )
    return a


def org_schema(a):
    if "photo" in a and a["photo"]:
        a["photo"] = f"{request.host_url}photo/{a['photo']}"
    return a
