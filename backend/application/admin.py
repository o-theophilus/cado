from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash, check_password_hash
from .tools import token_to_user, user_schema
from .storage import drive, storage


bp = Blueprint("admin", __name__)


permissions = {
    "user": [
        ['view', 1],
        ['set_permission', 3]
    ],
    "admin": [
        ['manage_photo', 3]
    ],
    "post": [
        ['add', 2],
        ['edit_photos', 2],
        ['edit_title', 2],
        ['edit_date', 2],
        ['edit_description', 2],
        ['edit_content', 2],
        ['edit_tags', 2],
        ['edit_status', 2],
        ['edit_author', 2],
        ['edit_highlight', 2]
    ],
    "report": [
        ['view', 1],
        ['edit_status', 3]
    ],
    "comment": [
        ['view_deleted', 1]
    ]
}


@bp.get("/admin/init")
def default_admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" ( key, status, name, email,
                    password, permissions)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
            key,
            "confirmed",
            "Theophilus",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in permissions for y in permissions[x]]
        ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/admin/permission")
@bp.get("/admin/permission/<search>")
def get_permission(search=None):
    _all = [f"{x}:{y[0]}" for x in permissions for y in permissions[x]]
    if search:
        _all = [x for x in _all if x.find(search) != -1]

    return jsonify({
        "status": 200,
        "permissions": _all
    })


@bp.put("/admin/permission/<key>")
def permission(key):
    con, cur = db_open()

    me = token_to_user(cur)
    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:set_permission" not in me["permissions"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "cannot be empty"
    elif not check_password_hash(me["password"], request.json["password"]):
        error = "incorrect password"
    elif (
        not user
        or me["key"] == user["key"]
        or "permissions" not in request.json
        or type(request.json["permissions"]) is not list
        or user["email"] == os.environ["MAIL_USERNAME"]
        or user["status"] != "confirmed"
    ):
        error = "invalid request"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    cur.execute("""
        UPDATE "user"
        SET permissions = %s
        WHERE key = %s;
    """, (
        request.json["permissions"],
        user["key"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/photo/error")
def photo_error():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT photo
        FROM "user";
    """)
    users_photo = cur.fetchall()
    users_photo = [x["photo"] for x in users_photo if x["photo"]]

    cur.execute("""
        SELECT photos
        FROM post;
    """)
    temp = cur.fetchall()
    posts_photos = []
    for x in temp:
        if x["photos"] != []:
            posts_photos += x["photos"]

    all_used_photos = users_photo + posts_photos
    paths = drive().list()["names"]
    all_stored_photos = [x.split('/')[1] for x in paths]

    cur.execute("""
        SELECT "user".key, "user".name
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_photos,))
    _users = cur.fetchall()

    cur.execute("""
        SELECT post.key, post.title
        FROM post
        WHERE NOT ARRAY[%s] @> photos;
    """, (all_stored_photos,))
    _posts = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "unused": [f"{request.host_url}photo/{x}"
                   for x in all_stored_photos if x not in all_used_photos],
        "users": _users,
        "posts": _posts
    })


@bp.delete("/photo/error")
def delete_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["permissions"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    if (
        "photos" not in request.json
        or type(request.json["photos"]) is not list
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    for x in request.json["photos"]:
        pass
        storage(x.split("/")[-1], delete=True)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
