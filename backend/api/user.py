from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, send_mail,
    generate_code, check_code)
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint("user", __name__)


@bp.put("/user")
def update():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "firstname" in request.json:
        if not request.json["firstname"]:
            error['firstname'] = "this field is required"
        user["firstname"] = request.json["firstname"].strip()

    if "lastname" in request.json:
        user["lastname"] = request.json["lastname"]

    if "phone" in request.json:
        phone = request.json["phone"]
        if phone:
            phone = phone.replace(' ', '')
            if not re.match(r'^\+?\d+$', phone):
                error['phone'] = """Invalid phone number. Phone number may
                    start with a '+' followed by digits"""
        user["phone"] = phone

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user"
        SET
            firstname = %s,
            lastname = %s,
            phone = %s
        WHERE key = %s
        RETURNING *;
    """, (
        user["firstname"],
        user["lastname"],
        user["phone"],
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/email/1")
def old_email_request_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        not request.json
        or user["email"] == os.environ["MAIL_USERNAME"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    send_mail(
        user["email"],
        "Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                user["email"]
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/2")
def old_email_check_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["email"] == os.environ["MAIL_USERNAME"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code_1": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/3")
def new_email_request_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if (
        error
        or user["email"] == os.environ["MAIL_USERNAME"]
        or not request.json
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "invalid email"
    elif user["email"] == request.json["email"]:
        error = "please use a different email form your current email"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "email is already in use"
        })

    send_mail(
        request.json["email"],
        "New Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                request.json["email"],
                False
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/4")
def new_email_check_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if (
        error
        or user["email"] == os.environ["MAIL_USERNAME"]
        or not request.json
        or "email" not in request.json
        or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
        or user["email"] == request.json["email"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute('SELECT * FROM "user" WHERE email = %s;',
                (request.json["email"],))
    exist = cur.fetchone()
    if exist:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], request.json["email"], "code_2")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (
        request.json["email"], user["key"]))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/password/1")
def password_request_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        not request.json
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    send_mail(
        user["email"],
        "Password Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                user["email"]
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/2")
def password_check_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/3")
def password():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"])
    if error or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """Password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""
    elif check_password_hash(user["password"], request.json["password"]):
        error["password"
              ] = "New password should be different from old password"

    if (
        "confirm_password" not in request.json
        or not request.json["confirm_password"]
    ):
        error["confirm_password"] = "this field is required"
    elif (
            request.json["password"]
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """Password and confirm_password password
         does not match"""
    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
