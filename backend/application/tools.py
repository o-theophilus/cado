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
import re
from mailjet_rest import Client


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
        admin = os.environ["MAIL_USERNAME"]

        msg = MIMEMultipart()
        msg['From'] = formataddr(("Urlinks", admin))
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


def send_mail_(
    to,
    # name,
    subject,
    body
):
    data = {
        'Messages': [
            {
                "From": {
                    "Email": os.environ["MAIL_USERNAME"],
                    "Name": "URLinks"
                },
                "To": [
                    {
                        "Email": to,
                        # "Name": name
                    }
                ],
                "Subject": subject,
                "HTMLPart": re.sub('&amp;', '&', body)
            }
        ]
    }

    if current_app.config["DEBUG"]:
        print(data)
    else:
        mailjet = Client(auth=(
            os.environ["MAILJET_API_KEY"],
            os.environ["MAILJET_SECRET_KEY"]),
            version='v3.1')

        result = mailjet.send.create(data=data)
        print(result.json())


def user_schema(user):
    del user["password"]
    user["photo"] = (
        f"{request.host_url}photo/{user['photo']}"
        if user["photo"] else None
    )
    return user
