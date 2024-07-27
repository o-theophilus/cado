from flask import Blueprint, jsonify, request
from .tools import (
    token_tool, token_to_user, user_schema, send_mail, reserved_words,
    generate_code, check_code, org_schema)
from uuid import uuid4
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .postgres import db_open, db_close

bp = Blueprint("account", __name__)


def anon(cur):
    key = uuid4().hex
    cur.execute("""
            INSERT INTO "user" (
                key, slug, firstname, lastname, email, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (
        key,
        key,
        key[:4],
        "user",
        uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"))
    )
    return cur.fetchone()


@bp.post("/init")
def init():
    con, cur = db_open()

    token = request.headers["Authorization"]
    user = token_to_user(cur)

    if not user or user["status"] == "confirmed" and not user["login"]:
        user = anon(cur)
        token = token_tool().dumps(user["key"])

    # TODO: wragby fix
    cur.execute(
        """SELECT * FROM organization WHERE email = %s;""",
        ("info@wragbysolutions.com",))
    org = cur.fetchone()
    if not org:
        org = {}

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token,
        "organization": org_schema(org)
    })


@bp.post("/signup")
def signup():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "firstname" not in request.json or not request.json["firstname"]:
        error["firstname"] = "this field is required"
    if "lastname" not in request.json or not request.json["lastname"]:
        error["lastname"] = "this field is required"

    _user = None

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (
            request.json["email"],))
        _user = cur.fetchone()
        if _user and _user["status"] == "confirmed":
            error["email"] = "email taken"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif (
        not re.search("[a-z]", request.json["password"])
        or not re.search("[A-Z]", request.json["password"])
        or not re.search("[0-9]", request.json["password"])
        or len(request.json["password"]) not in range(8, 19)
    ):
        error["password"] = """password must include at least 1 lowercase
        letter, 1 uppercase letter, 1 number and must contain 8 - 18
        characters"""

    if "confirm_password" not in request.json or not request.json[
            "confirm_password"]:
        error["confirm_password"] = "this field is required"
    elif (
            request.json["password"]
            and request.json["confirm_password"] != request.json["password"]
    ):
        error["confirm_password"] = """password and confirm password does not
        match"""

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if _user:
        user = _user
    elif user["status"] != "anonymous":
        user = anon(cur)

    slug = re.sub('-+', '-', re.sub(
        '[^a-zA-Z0-9]', '-',
        f"{request.json['firstname'][0]}{request.json['lastname']}".lower())
    )
    cur.execute('SELECT * FROM "user" WHERE key != %s AND slug = %s;',
                (user["key"], slug))
    if cur.fetchone() or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    # TODO: wragby fix
    cur.execute(
        """SELECT * FROM organization WHERE email = %s;""",
        ("info@wragbysolutions.com",))
    org = cur.fetchone()

    cur.execute("""
        UPDATE "user"
        SET
            slug = %s, firstname = %s, lastname = %s,
            email = %s, password = %s,
            organization_key = %s, office_location = %s
        WHERE key = %s
        RETURNING *;
    """, (
        slug,
        request.json["firstname"],
        request.json["lastname"],
        request.json["email"],
        generate_password_hash(request.json["password"], method="scrypt"),
        org["key"] if org else None,
        org["address"][0]["name"] if org and org["address"] != [] else None,
        user["key"]
    ))
    user = cur.fetchone()

    send_mail(
        user["email"],
        "Email Confirmation code",
        request.json['email_template'].format(
            firstname=user['firstname'],
            code=generate_code(
                cur,
                user["key"],
                user["email"],
                "signup"
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/confirm")
def confirm():
    con, cur = db_open()

    error = None
    if (
        "email" not in request.json
        or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user" SET status = 'confirmed' WHERE key = %s;
    """, (user["key"],))

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/login")
def login():
    con, cur = db_open()

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute(
        'SELECT * FROM "user" WHERE email = %s;',
        (request.json["email"],)
    )
    user = cur.fetchone()

    if (
        not user
        or not check_password_hash(
            user["password"], request.json["password"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    if user["status"] != "confirmed":
        send_mail(
            user["email"],
            "Email Confirmation code",
            request.json['email_template'].format(
                firstname=user["firstname"],
                code=generate_code(
                    cur,
                    user["key"],
                    user["email"],
                    "login"
                )
            )
        )
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        True, user["key"]
    ))

    out_user = token_to_user(cur)
    if out_user and out_user["status"] == 'anonymous':
        cur.execute(
            """DELETE FROM "user" WHERE key = %s;""",
            (out_user["key"],)
        )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "token": token_tool().dumps(user["key"])
    })


@bp.delete("/logout")
def logout():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        False, user["key"]
    ))

    user = anon(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token_tool().dumps(user["key"])
    })


@ bp.delete("/user/<key>")
def delete(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "password" not in request.json or not request.json["password"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "password": "this field is required"
        })

    if not check_password_hash(user["password"], request.json["password"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "incorrect password"
        })

    if user["key"] != key:
        if "user:delete" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""SELECT * FROM "user" WHERE key = %s;""", (key,))
            user = cur.fetchone()
            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    cur.execute("""DELETE FROM "user" WHERE key = %s;""", (user["key"],))

    user = anon(cur)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user),
        "token": token_tool().dumps(user["key"])
    })


@bp.post("/forgot/1")
def forgot_1_email():
    con, cur = db_open()

    if (
        "email_template" not in request.json
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
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "there is no user registered with this email"
        })

    send_mail(
        user["email"],
        "Password reset code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                user["email"],
                "forgot password"
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/forgot/2")
def forgot_2_code():
    con, cur = db_open()

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
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


@bp.post("/forgot/3")
def forgot_3_password():
    con, cur = db_open()

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM "user" WHERE email = %s
    ;""", (request.json["email"],))
    user = cur.fetchone()
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], user["email"])
    if error:
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
        UPDATE "user"
        SET
            password = %s,
            status = 'confirmed'
        WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
