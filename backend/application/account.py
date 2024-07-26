from flask import Blueprint, jsonify, request
from .tools import (
    token_tool, token_to_user, user_schema, send_mail, reserved_words,
    generate_code, check_code, org_schema)
from uuid import uuid4
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .postgres import db_open, db_close

bp = Blueprint("account", __name__)


@bp.post("/init")
def init():
    con, cur = db_open()

    token = request.headers["Authorization"]
    user = token_to_user(cur)

    if not user or user["status"] == "confirmed" and not user["login"]:
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
        user = cur.fetchone()

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

    print(1)
    user = token_to_user(cur)
    if not user:
        print(2)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    print(3)
    if (
        user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        print(4)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    print(5)
    error = {}

    if "firstname" not in request.json or not request.json["firstname"]:
        error["firstname"] = "this field is required"
    if "lastname" not in request.json or not request.json["lastname"]:
        error["lastname"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "Please enter a valid email"

    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;', (
            request.json["email"],))
        if cur.fetchone():
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

    print(6)
    if error != {}:
        print(7)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    print(8)
    if user["status"] != "anonymous":
        key = uuid4().hex
        cur.execute("""
            INSERT INTO "user" (
                key, slug, firstname, lastname, email, password)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (
            key,
            key,
            f"user_{key[:4]}",
            f"user_{key[-4:]}",
            uuid4().hex,
            generate_password_hash(uuid4().hex, method="scrypt")))

    print(9)
    _name = f"{request.json['firstname'][0]}{request.json['lastname']}"
    slug = re.sub(
        '-+', '-', re.sub(
            '[^a-zA-Z0-9]', '-',
            _name.lower()
        )
    )
    cur.execute('SELECT * FROM "user" WHERE slug = %s;', (slug,))
    if cur.fetchone() or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    # TODO: wragby fix
    print(10)
    cur.execute(
        """SELECT * FROM organization WHERE email = %s;""",
        ("info@wragbysolutions.com",))
    org = cur.fetchone()

    print(11)
    cur.execute("""
        UPDATE "user"
        SET
            slug = %s, organization_key = %s, firstname = %s, lastname = %s,
            email = %s, password = %s, status = 'signedup'
        WHERE key = %s
        RETURNING *;
    """, (
        slug,
        org["key"] if org else None,
        request.json["firstname"],
        request.json["lastname"],
        request.json["email"],
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))
    user = cur.fetchone()
    print(12)

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
    print(13)

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
    if not user or user["status"] != 'signedup':
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

    print(1)
    out_user = token_to_user(cur)
    if not out_user:
        print(2)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    print(3)
    if (
        out_user["login"]
        or "email_template" not in request.json
        or not request.json["email_template"]
    ):
        print(4)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    print(5)
    error = {}
    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"

    if error != {}:
        print(6)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    in_user = None
    if out_user["email"] == request.json["email"]:
        in_user = out_user
    else:
        cur.execute('SELECT * FROM "user" WHERE email = %s;',
                    (request.json["email"],))
        in_user = cur.fetchone()

    if (
        not in_user
        or in_user["status"] not in ['signedup', 'confirmed']
        or not check_password_hash(
            in_user["password"], request.json["password"])
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "your email or password is incorrect"
        })

    print(7)
    if in_user["status"] != "confirmed":
        send_mail(
            in_user["email"],
            "Email Confirmation code",
            request.json['email_template'].format(
                firstname=in_user["firstname"],
                code=generate_code(
                    cur,
                    in_user["key"],
                    in_user["email"],
                    "login"
                )
            )
        )
        print(8)
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not confirmed"
        })

    print(9)
    cur.execute("""
        UPDATE "user" SET login = %s
        WHERE key = %s RETURNING *;""", (
        True, in_user["key"]
    ))
    print(10)
    cur.execute("""
        UPDATE "user"
        SET status = 'deleted', login = %s
        WHERE key = %s AND status = 'anonymous'
        RETURNING *;""", (
        False, out_user["key"]
    ))

    print(11)
    db_close(con, cur)
    return jsonify({
        "status": 200,
        "token": token_tool().dumps(in_user["key"])
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

    key = uuid4().hex
    cur.execute("""
        INSERT INTO "user" (
            key, slug, firstname, lastname, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        key,
        key,
        f"user_{key[:4]}",
        f"user_{key[-4:]}",
        uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt")
    ))
    anon_user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
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
    if not user or user["status"] not in ['signedup', 'confirmed']:
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
    if not user or user["status"] not in ['signedup', 'confirmed']:
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
    if not user or user["status"] not in ['signedup', 'confirmed']:
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
        UPDATE "user" SET password = %s WHERE key = %s;
    """, (
        generate_password_hash(request.json["password"], method="scrypt"),
        user["key"]
    ))

    if user["status"] != "confirmed":
        cur.execute("""
            UPDATE "user" SET status = 'confirmed' WHERE key = %s;
        """, (user["key"],))

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
