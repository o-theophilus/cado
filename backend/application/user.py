from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, send_mail, token_tool, reserved_words,
    generate_otp, check_otp)
from uuid import uuid4
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage
from .account import organization


bp = Blueprint("user", __name__)


@bp.put("/user/details/<key>")
def edit_details(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or user["key"] != key:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "firstname" not in request.json or not request.json["firstname"]:
        error['firstname'] = "cannot be empty"
    if "lastname" not in request.json or not request.json["lastname"]:
        error['lastname'] = "cannot be empty"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    role = None
    phone = None
    manager_email = None
    about_me = None
    office_location = None
    if "role" in request.json and request.json["role"]:
        role = request.json["role"]
    if "phone" in request.json and request.json["phone"]:
        phone = request.json["phone"]
    if "manager_email" in request.json and request.json["manager_email"]:
        manager_email = request.json["manager_email"]
    if "about_me" in request.json and request.json["about_me"]:
        about_me = request.json["about_me"]
    if "office_location" in request.json and request.json["office_location"]:
        office_location = request.json["office_location"]

    slug = user["slug"]
    if (
        user["firstname"] != request.json["firstname"]
        or user["lastname"] != request.json["lastname"]
    ):
        _name = f"{request.json['firstname'][0]}{request.json['lastname']}"
        slug = re.sub(
            '-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-',
                _name.lower()
            )
        )
        cur.execute('SELECT * FROM "user" WHERE key != %s AND slug = %s;',
                    (user["key"], slug))
        if cur.fetchone() or slug in reserved_words:
            slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        UPDATE "user"
        SET
            slug = %s,
            firstname = %s,
            lastname = %s,
            role = %s,
            phone = %s,
            manager_email = %s,
            about_me = %s,
            office_location = %s
        WHERE key = %s
        RETURNING *;
    """, (
        slug,
        request.json["firstname"],
        request.json["lastname"],
        role,
        phone,
        manager_email,
        about_me,
        office_location,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user/links/<key>")
def edit_links(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user or user["key"] != key:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    whatsapp = None
    linkedin = None
    twitter = None
    facebook = None
    instagram = None
    if "whatsapp" in request.json and request.json["whatsapp"]:
        whatsapp = request.json["whatsapp"]
    if "linkedin" in request.json and request.json["linkedin"]:
        linkedin = request.json["linkedin"]
    if "twitter" in request.json and request.json["twitter"]:
        twitter = request.json["twitter"]
    if "facebook" in request.json and request.json["facebook"]:
        facebook = request.json["facebook"]
    if "instagram" in request.json and request.json["instagram"]:
        instagram = request.json["instagram"]

    slug = user["slug"]
    if (
        user["firstname"] != request.json["firstname"]
        or user["lastname"] != request.json["lastname"]
    ):
        _name = f"{request.json['firstname'][0]}{request.json['lastname']}"
        slug = re.sub(
            '-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-',
                _name.lower()
            )
        )
        cur.execute('SELECT * FROM "user" WHERE key != %s AND slug = %s;',
                    (user["key"], slug))
        if cur.fetchone() or slug in reserved_words:
            slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        UPDATE "user"
        SET
            whatsapp = %s,
            linkedin = %s,
            twitter = %s,
            facebook = %s,
            instagram = %s
        WHERE key = %s
        RETURNING *;
    """, (
        whatsapp,
        linkedin,
        twitter,
        facebook,
        instagram,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/email/1")
def email_1_old_email():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    send_mail(
        user["email"],
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            name=user["name"],
            otp=generate_otp(cur, user["key"], user["email"], "change email")
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/2")
def email_2_old_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_otp(cur, user["key"], user["email"], "otp_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "otp_1": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/3")
def email_3_new_email():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_otp(cur, user["key"], user["email"], "otp_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

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
        error = "cannot be empty"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "invalid email"
    elif organization["email_domain"] != [] and not request.json[
            "email"].endswith(tuple(organization["email_domain"])):
        error["email"
              ] = f"Please enter a valid {organization["name"]} email address"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    if user["email"] == request.json["email"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": "please use a different email form your current email"
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
        "Email Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            firstname=user["firstname"],
            otp=generate_otp(
                cur,
                user["key"],
                request.json["email"],
                "change email",
                False
            ),
            organization_name=organization["name"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/4")
def email_4_new_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_otp(cur, user["key"], user["email"], "otp_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
        or (
            organization["email_domain"] != [] and not request.json[
            "email"].endswith(tuple(organization["email_domain"]))
        )
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["email"] == request.json["email"]:
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

    error = check_otp(cur, user["key"], request.json["email"], "otp_2")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "LoL"
        })

    cur.execute("""
        UPDATE "user" SET email = %s WHERE key = %s RETURNING *;
    """, (
        request.json["email"], user["key"]))
    user = cur.fetchone()

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@ bp.post("/user/password/1")
def password_1_email():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if (
        "email_template" not in request.json
        or not request.json["email_template"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    send_mail(
        user["email"],
        "Password Change Confirmation - One-Time Password (OTP)",
        request.json['email_template'].format(
            firstname=user["firstname"],
            otp=generate_otp(
                cur,
                user["key"],
                user["email"],
                "change password"
            ),
            organization_name=organization["name"]
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@ bp.post("/user/password/2")
def password_2_otp():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_otp(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "otp": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@ bp.post("/user/password/3")
def password_3_password():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_otp(cur, user["key"], user["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"
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
        error["confirm_password"] = "cannot be empty"
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

    cur.execute("DELETE FROM otp WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@ bp.delete("/user")
def delete():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "cannot be empty"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if not check_password_hash(user["password"], request.json["password"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "incorrect password"
        })

    cur.execute("""
        UPDATE "user"
        SET status = 'deleted', login = %s, permissions = %s
        WHERE key = %s;
    """, (
        False,
        [],
        user["key"]
    ))

    cur.execute("""
        INSERT INTO "user" (key, version, email, password, setting_theme)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex, uuid4().hex, uuid4().hex,
        generate_password_hash(uuid4().hex, method="scrypt"),
        user["setting_theme"]
    ))
    anon_user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(anon_user),
        "token": token_tool().dumps(anon_user["key"])
    })


@ bp.put("/user/photo")
def add_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if 'file' not in request.files:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    file = request.files["file"]
    media, _format = file.content_type.split("/")
    if media != "image" or _format in ['svg+xml', 'x-icon']:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid file"
        })

    if user["photo"]:
        storage(user["photo"], delete=True)

    file_name = storage(file)

    cur.execute("""
        UPDATE "user"
        SET photo = %s
        WHERE key = %s
        RETURNING *;
    """, (
        file_name,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@ bp.delete("/user/photo")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["photo"]:
        storage(user["photo"].split("/")[-1], delete=True)

        cur.execute("""
            UPDATE "user"
            SET photo = NULL
            WHERE key = %s;
        """, (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
