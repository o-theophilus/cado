from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, send_mail,
    generate_code, check_code)
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from math import ceil
from .admin import access


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


# TODO: this is not used, remove it
@bp.get("/user/<key>")
def get(key, cur=None):

    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("""
        WITH
        org AS (
            SELECT
                user_organization.user_key,
                user_organization.status AS _status,
                organization.*

            FROM user_organization
            LEFT JOIN organization
                ON user_organization.organization_key = organization.key
            WHERE organization.status = 'live'
        )

        SELECT "user".*,
            org._status as organization_status,
            jsonb_build_object(
                'key', org.key,
                'status', org.status,
                'slug', org.slug,
                'name', org.name,
                'fullname', org.fullname,
                'slogan', org.slogan,
                'email_domains', org.email_domains,
                'phone', org.phone,
                'email', org.email,
                'website', org.website,
                'address', org.address,
                'whatsapp', org.whatsapp,
                'linkedin', org.linkedin,
                'facebook', org.facebook,
                'twitter', org.twitter,
                'instagram', org.instagram,
                'logo', org.logo,
                'icon', org.icon
            ) AS organization
        FROM "user"
        LEFT JOIN org
            ON "user".key = "org".user_key
        WHERE "user".key = %s
        GROUP BY "user".key, org.user_key, org._status,
        org.key, org.status, org.slug, org.name, org.fullname,
        org.slogan, org.email_domains, org.phone, org.email,
        org.website, org.address, org.whatsapp, org.linkedin,
        org.facebook, org.twitter, org.instagram, org.logo, org.icon
    ;""", (key))
    user = cur.fetchone()

    if not user:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/users")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'name (a-z)': 'firstname',
        'name (z-a)': 'firstname'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "confirmed"
    search = ""
    page_no = 1
    page_size = 24

    if "status" in request.args:
        status = request.args["status"]
    if "search" in request.args:
        search = request.args["search"].strip()
    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])

    cur.execute("""
        SELECT
            *,
            COUNT(*) OVER() AS _count
        FROM "user"
        WHERE
            (
                %s = '' OR status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', key, firstname, lastname, email
                ) ILIKE %s
            )
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'confirmed'],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })


@bp.get("/admin/user")
def get_admins():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:edit_access" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'name (a-z)': 'firstname',
        'name (z-a)': 'firstname'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    page_no = 1
    page_size = 24
    search = ":all:all"

    if "order" in request.args:
        order = request.args["order"]
    if "page_no" in request.args:
        page_no = int(request.args["page_no"])
    if "size" in request.args:
        page_size = int(request.args["size"])
    if "search" in request.args:
        search = request.args["search"]
    search = search.split(":")
    if len(search) != 3:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid search"
        })
    user_key, _type, _action = search
    user_key = user_key.strip()

    cur.execute("""
        SELECT
            *,
            COUNT(*) OVER() AS _count
        FROM "user"
        WHERE
            array_length(access, 1) IS NOT NULL
            AND status = 'confirmed'
            AND (%s = ''
                OR CONCAT_WS(', ', key, firstname, lastname, email)
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
            AND (%s = 'all' OR ARRAY_TO_STRING(access, ',')
                ILIKE %s)
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        user_key, f"%{user_key}%",
        _type, f"%{_type}:%",
        _action, f"%{_type}:{_action}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    asx = {
        "all": ['all']
    }
    for x in access:
        if x not in asx:
            asx[x] = ["all"]
            for y in access[x]:
                asx[x].append(y[0])

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "access": asx,
        "order_by": list(order_by.keys()),
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })
