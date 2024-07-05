from flask import request, current_app
from itsdangerous import URLSafeTimedSerializer
import smtplib
from email.utils import formataddr
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from uuid import uuid4
import random
from datetime import datetime, timedelta


reserved_words = ["app", "wragby", "home",
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


def generate_otp(cur, key, email, _from, clear=True):
    if clear:
        cur.execute("DELETE FROM otp WHERE user_key = %s;", (key,))

    otp = f"{random.randint(100000, 999999)}"
    otp_key = uuid4().hex

    cur.execute("""
        INSERT INTO otp (key, date, user_key, pin, email)
        VALUES (%s, %s, %s, %s, %s);
    """, (
        otp_key,
        datetime.now(),
        key,
        otp,
        email
    ))

    return otp


def check_otp(cur, key, email, n="otp"):
    error = None
    if n not in request.json or not request.json[n]:
        error = "cannot be empty"
    elif len(request.json[n]) != 6:
        error = "invalid OTP"

    cur.execute("""
        SELECT *
        FROM otp
        WHERE
            otp.user_key = %s
            AND otp.pin = %s
            AND otp.email = %s;
    """, (
        key,
        request.json[n],
        email
    ))
    otp = cur.fetchone()

    if not otp:
        error = "invalid OTP"
    elif datetime.now() - otp["date"] > timedelta(minutes=15):
        cur.execute("""
            DELETE FROM otp WHERE user_key = %s
        ;""", (key,))
        error = "invalid OTP"

    return error


def send_mail(to, subject, body):
    # if current_app.config["DEBUG"]:
    #     print(body)
    # else:
    admin = os.environ["MAIL_USERNAME"]

    print("sending")
    msg = MIMEMultipart()
    msg['From'] = formataddr(("Meji", admin))
    msg['To'] = to
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'html'))

    server = smtplib.SMTP('smtp.office365.com', 587)
    server.starttls()
    server.login(
        admin,
        os.environ["MAIL_PASSWORD"]
    )
    server.sendmail(admin, to, msg.as_bytes())
    server.quit()


def user_schema(user):
    del user["password"]
    user["photo"] = (
        f"{request.host_url}photo/{user['photo']}"
        if user["photo"] else None
    )
    return user
