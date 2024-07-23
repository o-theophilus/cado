from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash, check_password_hash
from .tools import token_to_user, user_schema
from .storage import drive, storage


bp = Blueprint("admin", __name__)

access = {
    "user": [
        ['view', 1],
        ['edit_photo', 2],
        ['edit_personal', 2],
        ['edit_organization', 2],
        ['edit_contact', 2],
        ['edit_social_media', 2],
        ['edit_access', 3],
        ['delete', 3]
    ],
    "admin": [
        ['view_photo_error', 2]
    ],
    "organization": [
        ['view', 1],
        ['add', 2],
        ['edit_logo', 2],
        ['edit_icon', 2],
        ['edit_organization', 2],
        ['edit_contact', 2],
        ['edit_social_media', 2],
        # ['delete', 3]
    ],
}


@bp.get("/admin/access")
@bp.get("/admin/access/<search>")
def get_access(search=None):
    out = access
    if search:
        out = [f"{x}:{y[0]}" for x in access for y in access[x]]
        if search != "all":
            out = [x for x in out if x.find(search) != -1]

    return jsonify({
        "status": 200,
        "access": out
    })


@bp.put("/admin/access/<key>")
def set_access(key):
    con, cur = db_open()

    me = token_to_user(cur)
    cur.execute('SELECT * FROM "user" WHERE key = %s;', (key,))
    user = cur.fetchone()

    error = None
    if not me or "user:edit_access" not in me["access"]:
        error = "unauthorized access"
    elif "password" not in request.json:
        error = "cannot be empty"
    elif not check_password_hash(me["password"], request.json["password"]):
        error = "incorrect password"
    elif (
        not user
        or me["key"] == user["key"]
        or "access" not in request.json
        or type(request.json["access"]) is not list
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
        SET access = %s
        WHERE key = %s;
    """, (
        request.json["access"],
        user["key"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "user": user_schema(user)
    })


@bp.get("/admin/init")
def default_admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" (
                    key, status, slug, firstname,
                    lastname, email, password, access)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
            """, (
            key,
            "confirmed",
            "urlinks",
            "UR",
            "Links",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt"),
            [f"{x}:{y[0]}" for x in access for y in access[x]]
        ))

    db_close(con, cur)
    return jsonify({
        "status": 200
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

    if "admin:view_photo_error" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    paths = drive().list()["names"]
    all_stored_photos = [x.split('/')[1] for x in paths]

    cur.execute("""
        SELECT slug, firstname, lastname
        FROM "user"
        WHERE
            photo IS NOT NULL
            AND NOT photo = ANY(%s);
    """, (all_stored_photos,))
    _users = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "users": _users
    })


def clean_photo():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "admin:manage_photo" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT photo
        FROM "user";
    """)
    users_photo = [x["photo"] for x in cur.fetchall() if x["photo"]]

    paths = drive().list()["names"]
    for x in paths:
        if x.split('/')[1] not in users_photo:
            storage(x, delete=True)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
