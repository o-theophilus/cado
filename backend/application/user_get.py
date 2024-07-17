from flask import Blueprint, request, jsonify
from .tools import token_to_user, user_schema
from math import ceil
from .postgres import db_close, db_open


bp = Blueprint("user_get", __name__)


@bp.get("/user/<key>")
def get(key):
    con, cur = db_open()

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
            "error": "invalid token"
        })

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
        'name (a-z)': '"user".firstname',
        'name (z-a)': '"user".firstname'
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
    print(users)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": [user_schema(x) for x in users],
        "order_by": list(order_by.keys()),
        "_status": ['anonymous', 'signedup', 'confirmed'],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })
