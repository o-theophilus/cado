from flask import Blueprint, jsonify, request
from uuid import uuid4
import os
from .postgres import db_open, db_close
from werkzeug.security import generate_password_hash
from .tools import token_to_user
from .storage import drive, storage


bp = Blueprint("admin", __name__)


@bp.get("/admin/init")
def default_admin():
    con, cur = db_open()
    email = os.environ["MAIL_USERNAME"]

    cur.execute('SELECT * FROM "user" WHERE email = %s;', (email,))
    if not cur.fetchone():
        key = uuid4().hex
        cur.execute("""
                INSERT INTO "user" (
                    key, slug, firstname, lastname, email, password)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (
            key,
            "urlinks",
            "UR",
            "Links",
            email,
            generate_password_hash(
                os.environ["MAIL_PASSWORD"], method="scrypt")
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
