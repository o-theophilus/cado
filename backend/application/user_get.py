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

    if "user:view" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    order_by = {
        'latest': 'log.date',
        'oldest': 'log.date',
        'name (a-z)': '"user".name',
        'name (z-a)': '"user".name'
    }

    order_dir = {
        'latest': 'DESC',
        'oldest': 'ASC',
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = ""
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
            log.date AS date,
            COUNT(*) OVER() AS _count
        FROM "user"
        LEFT JOIN log ON
            "user".key = log.user_key
            AND log.action = 'created'
            AND log.entity_type = 'account'
        WHERE
            (
                %s = '' OR "user".status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', "user".key, "user".name, "user".email
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
        "_status": ['anonymous', 'signedup', 'confirmed'],
        "total_page": ceil(users[0]["_count"] / page_size) if users else 0
    })
