from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (token_to_user, user_schema, check_code, reserved_words,
                    send_mail, generate_code)
from uuid import uuid4
from math import ceil
from .organization_get import get_many
from .user_get import get
import re


bp = Blueprint("user_organization", __name__)


# TODO:'
# user can request to join org
# user can exit org
# admin can add user to org [user:org_add_user]
# admin can accept user to org [user:org_accept_user]
# admin can remove user rom org [user:org_remove_user]


@bp.post("/organization/join/<key>")
def join_existing(key):
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

    cur.execute("""
        SELECT *
        FROM user_organization
        WHERE user_key = %s;
    """, (key,))
    if cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    org = None
    if "key" in request.json and request.json["key"]:
        cur.execute("""
            SELECT * FROM organization WHERE key = %s;
        """, (request.json["key"],))
        org = cur.fetchone()
        if not org:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    cur.execute("""
        INSERT INTO user_organization (
            key, status, user_key, organization_key)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid4().hex,
        "pending",
        user["key"],
        org["key"]
    ))

    user = get(user["key"], cur).json["user"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })


@bp.post("/organization/add/1")
def add__request_code():
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

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "invalid email"
    if "email" not in error:
        cur.execute('SELECT * FROM organization WHERE email = %s;', (
            request.json["email"],))
        if cur.fetchone():
            error["email"] = "email taken"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    send_mail(
        request.json["email"],
        "Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                request.json["email"],
                "add organization"
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/organization/add/2")
def add__submit_code():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "invalid email"
    if "email" not in error:
        cur.execute('SELECT * FROM organization WHERE email = %s;', (
            request.json["email"],))
        if cur.fetchone():
            error["email"] = "email taken"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    error = check_code(cur, user["key"], request.json["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "code": error
        })

    slug = re.sub(
        '-+', '-', re.sub(
            '[^a-zA-Z0-9]', '-',
            request.json['name'].lower()
        )
    )
    cur.execute('SELECT * FROM organization WHERE slug = %s;', (slug,))
    if cur.fetchone() or slug in reserved_words:
        slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        INSERT INTO organization (key, slug, name, fullname, email)
        VALUES (%s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex,
        slug,
        request.json["name"],
        request.json["name"],
        request.json["email"]
    ))
    org = cur.fetchone()

    cur.execute("""
        INSERT INTO user_organization (
            key, status, user_key, organization_key)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid4().hex,
        "approved",
        user["key"],
        org["key"]
    ))

    user = get(user["key"], cur).json["user"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })


@bp.delete("/organization/delete/<key>")
def cancel(key):
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

    cur.execute("""
        SELECT * FROM user_organization WHERE user_key = %s;
    """, (user["key"],))
    user_org = cur.fetchone()
    cur.execute("""
        SELECT * FROM user_organization WHERE organization_key = %s;
    """, (user_org["organization_key"],))
    members = cur.fetchall()
    if len(members < 2):
        cur.execute(
            """DELETE FROM organization WHERE key = %s;""",
            (user_org["organization_key"],))

    cur.execute(
        """DELETE FROM user_organization WHERE user_key = %s;""",
        (user["key"],))

    user = get(user["key"], cur).json["user"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user
    })


@bp.get("/organization/users/<key>")
def get_org_users(key, cur=None):

    close_conn = False
    if not cur:
        con, cur = db_open()
        close_conn = True

    user = token_to_user(cur)
    if not user:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "user:view" not in user["access"]:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    # TODO: add date
    order_by = {
        'name (a-z)': 'firstname',
        'name (z-a)': 'firstname'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "accepted"
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
            "user".*,
            COUNT(*) OVER() AS _count
        FROM user_organization
        LEFT JOIN "user" ON user_organization.user_key = "user".key
        WHERE
            user_organization.organization_key = %s
            AND (
                %s = '' OR user_organization.status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', "user".key, "user".firstname,
                "user".lastname, "user".email
                ) ILIKE %s
            )
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        key,
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    users = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['pending', 'approved', "rejected"],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })


@bp.post("/organization/approve/<key>")
def approve(key):
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

    cur.execute("""
        SELECT *
        FROM user_organization
        WHERE user_key = %s AND status = 'pending';
    """, (key,))
    if not cur.fetchone():
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    org = None
    if ("organization_key" in
            request.json and request.json["organization_key"]):
        cur.execute("""
            SELECT * FROM organization WHERE key = %s;
        """, (request.json["organization_key"],))
        org = cur.fetchone()
        if not org or "approved" not in request.json:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "invalid request"
            })

    cur.execute("""
        UPDATE user_organization SET status = %s WHERE key = %s;
    """, (
        "approved" if request.json["organization_key"] else "rejected",
        org["key"]
    ))

    temp = get_many(request.json["organization_key"], cur).json
    db_close(con, cur)
    return jsonify({
        "status": 200,
        **temp
    })
