from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, send_mail, reserved_words,
    generate_code, check_code)
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage


bp = Blueprint("user", __name__)


@bp.put("/user/personal/<key>")
def personal(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_personal" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    error = {}

    if "firstname" not in request.json or not request.json["firstname"]:
        error['firstname'] = "this field is required"
    if "lastname" not in request.json or not request.json["lastname"]:
        error['lastname'] = "this field is required"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    about_me = None
    if "about_me" in request.json and request.json["about_me"]:
        about_me = request.json["about_me"]
    role = None
    if "role" in request.json and request.json["role"]:
        role = request.json["role"]

    cur.execute("""
        UPDATE "user"
        SET
            firstname = %s,
            lastname = %s,
            role = %s,
            about_me = %s
        WHERE key = %s
        RETURNING *;
    """, (
        request.json["firstname"].strip(),
        request.json["lastname"].strip(),
        role,
        about_me,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


# TODO: remove this if not using manager's email
@bp.put("/user/role/<key>")
def role(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_organization" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    # TODO: role to job title
    organization_key = None
    role = None
    manager_email = None

    # if "organization_key" in
    #  request.json and request.json["organization_key"]:
    #     cur.execute("""
    #         SELECT * FROM organization WHERE key = %s;
    #     """, (request.json["organization_key"],))
    #     org = cur.fetchone()
    #     if org:
    #         organization_key = org["key"]

    if "role" in request.json and request.json["role"]:
        role = request.json["role"]
    if "manager_email" in request.json and request.json["manager_email"]:
        manager_email = request.json["manager_email"]

    cur.execute("""
        UPDATE "user"
        SET
            organization_key = %s,
            role = %s,
            manager_email = %s
        WHERE key = %s
        RETURNING *;
    """, (
        organization_key,
        role,
        manager_email,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user/contact/<key>")
def contact(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_contact" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    phone = None
    office_location = None
    if "phone" in request.json and request.json["phone"]:
        phone = request.json["phone"]
    if "office_location" in request.json and request.json["office_location"]:
        office_location = request.json["office_location"]

    cur.execute("""
        UPDATE "user"
        SET
            phone = %s,
            office_location = %s
        WHERE key = %s
        RETURNING *;
    """, (
        phone,
        office_location,
        user["key"]
    ))
    user = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.put("/user/social/<key>")
def social(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_social_media" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    whatsapp = None
    linkedin = None
    twitter = None
    facebook = None
    instagram = None
    if "whatsapp" in request.json and request.json["whatsapp"]:
        whatsapp = request.json["whatsapp"].replace(' ', '')
        if not re.match(r'^\+\d{1,3}\d*$', whatsapp):
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "whatsapp":  """Invalid phone number. Phone number should \
                    start with a "+" followed by the country code and then \
                    the phone number. For example, +2348012345678."""
            })

    if "linkedin" in request.json and request.json["linkedin"]:
        linkedin = request.json["linkedin"]
    if "twitter" in request.json and request.json["twitter"]:
        twitter = request.json["twitter"]
    if "facebook" in request.json and request.json["facebook"]:
        facebook = request.json["facebook"]
    if "instagram" in request.json and request.json["instagram"]:
        instagram = request.json["instagram"]

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


@bp.put("/user/slug/<key>")
def edit_slug(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}
    if "slug" not in request.json or not request.json["slug"]:
        error["error"] = "invalid request"
    elif "user:edit_slug" not in user["access"]:
        error["error"] = "unauthorized access"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif not check_password_hash(user["password"], request.json["password"]):
        error["password"] = "incorrect password"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    if user["key"] != key:
        cur.execute("""
            SELECT *
            FROM "user"
            WHERE slug = %s OR email = %s OR key = %s;
        """, (key, key, key))
        user = cur.fetchone()
        if not user:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    slug = re.sub(
        '-+', '-', re.sub(
            '[^a-zA-Z0-9]', '-',
            request.json["slug"].strip().lower()
        )
    )
    cur.execute('SELECT * FROM "user" WHERE key != %s AND slug = %s;',
                (user["key"], slug))
    if cur.fetchone() or slug in reserved_words:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "slug": "not available"
        })

    cur.execute("""
        UPDATE "user" SET slug = %s WHERE key = %s RETURNING *;
    """, (slug, user["key"]))
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
        "Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                user["email"],
                "change email"
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/2")
def email_2_old_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
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
def email_3_new_email():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
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

    cur.execute("""
        SELECT * FROM organization WHERE key = %s;
    """, (user["organization_key"],))
    org = cur.fetchone()

    error = None
    if "email" not in request.json or not request.json["email"]:
        error = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error = "invalid email"
    elif (
        org
        and org["email_domains"] != []
        and not request.json["email"].endswith(tuple(org["email_domains"]))
    ):
        error = f"Please enter a valid {org['name']} email address"
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
        "New Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                request.json["email"],
                "change email",
                False
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/email/4")
def email_4_new_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = check_code(cur, user["key"], user["email"], "code_1")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM organization WHERE key = %s;
    """, (user["organization_key"], user["organization_key"]))
    org = cur.fetchone()

    if (
        "email" not in request.json or not request.json["email"]
        or not re.match(r"\S+@\S+\.\S+", request.json["email"])
        or (
            org
            and org["email_domains"] != []
            and not request.json["email"].endswith(tuple(org["email_domains"]))
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

    error = check_code(cur, user["key"], request.json["email"], "code_2")
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if user["email"] == os.environ["MAIL_USERNAME"]:
        cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))
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

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.post("/user/password/1")
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
        "Password Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                user["email"],
                "change password"
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/user/password/2")
def password_2_code():
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
def password_3_password():
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


@bp.put("/user/photo/<key>")
def add_photo(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_photo" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
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
        storage("delete", user["photo"])

    file_name = storage("save", file)

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


@bp.delete("/user/photo/<key>")
def delete_photo(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if user["key"] != key:
        if "user:edit_photo" not in user["access"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "unauthorized access"
            })
        else:
            cur.execute("""
                SELECT *
                FROM "user"
                WHERE slug = %s OR email = %s OR key = %s;
            """, (key, key, key))
            user = cur.fetchone()

            if not user:
                db_close(con, cur)
                return jsonify({
                    "status": 400,
                    "error": "invalid request"
                })

    if user["photo"]:
        storage("delete", user["photo"].split("/")[-1])

        cur.execute("""
            UPDATE "user"
            SET photo = NULL
            WHERE key = %s;
        """, (user["key"],))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
