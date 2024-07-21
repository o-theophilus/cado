from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema,  token_tool, reserved_words)
from uuid import uuid4
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage


bp = Blueprint("org", __name__)


@bp.post("/organization")
def add():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "organization:add" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
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
            INSERT INTO organization (
                key, slug, name, email)
            VALUES (%s, %s, %s, %s)
            RETURNING *;
        """, (
        uuid4().hex,
        slug,
        request.json["name"],
        request.json["email"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org
    })


@ bp.put("/organization/org/<key>")
def _organization(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "organization:edit_organization" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT *
        FROM organization
        WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()
    if not org:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    name = None
    fullname = None
    slogan = None
    if "name" in request.json and request.json["name"]:
        name = request.json["name"]
    if "fullname" in request.json and request.json["fullname"]:
        fullname = request.json["fullname"]
    if "slogan" in request.json and request.json["slogan"]:
        slogan = request.json["slogan"]

    slug = org["slug"]
    if org["name"] != request.json["name"]:
        slug = re.sub(
            '-+', '-', re.sub(
                '[^a-zA-Z0-9]', '-',
                request.json['name'].lower()
            )
        )
        cur.execute(
            'SELECT * FROM organization WHERE key != %s AND slug = %s;',
            (org["key"], slug))
        if cur.fetchone() or slug in reserved_words:
            slug = f"{slug}-{str(uuid4().hex)[:10]}"

    cur.execute("""
        UPDATE organization
        SET
            slug = %s,
            name = %s,
            fullname = %s,
            slogan = %s
        WHERE key = %s
        RETURNING *;
    """, (
        slug,
        name,
        fullname,
        slogan,
        org["key"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org
    })


@ bp.put("/organization/contact/<key>")
def contact(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "organization:edit_contact" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT *
        FROM organization
        WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()
    if not org:
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

    if not error:
        cur.execute(
            'SELECT * FROM organization WHERE key != %s AND email = %s;', (
                org["key"], request.json["email"]
            )
        )
        if cur.fetchone():
            error = "email taken"

    if (
        not error
        and org["email_domains"] != []
        and not request.json["email"].endswith(tuple(org["email_domains"]))
    ):
        error = "invalid email domain"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": error
        })

    phone = None
    website = None
    if "phone" in request.json and request.json["phone"]:
        phone = request.json["phone"]
    if "website" in request.json and request.json["website"]:
        website = request.json["website"]

    cur.execute("""
        UPDATE organization
        SET
            phone = %s,
            email = %s,
            website = %s,
            address = %s
        WHERE key = %s
        RETURNING *;
    """, (
        phone,
        request.json["email"],
        website,
        request.json["address"],
        org["key"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org
    })


@ bp.put("/organization/social/<key>")
def social(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "organization:edit_social_media" not in user["access"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "unauthorized access"
        })

    cur.execute("""
        SELECT *
        FROM organization
        WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()
    if not org:
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
        whatsapp = request.json["whatsapp"]
    if "linkedin" in request.json and request.json["linkedin"]:
        linkedin = request.json["linkedin"]
    if "twitter" in request.json and request.json["twitter"]:
        twitter = request.json["twitter"]
    if "facebook" in request.json and request.json["facebook"]:
        facebook = request.json["facebook"]
    if "instagram" in request.json and request.json["instagram"]:
        instagram = request.json["instagram"]

    cur.execute("""
        UPDATE organization
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
        org["key"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org
    })


@ bp.delete("/organization/<key>")
def delete(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if "password" not in request.json or not request.json["password"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "password": "this field is required"
        })

    if not check_password_hash(user["password"], request.json["password"]):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "incorrect password"
        })

    if user["key"] != key:
        if "user:delete" not in user["access"]:
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

    cur.execute("""DELETE FROM "user" WHERE key = %s;""", (user["key"],))

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


@ bp.put("/organization/photo/<key>")
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


@ bp.delete("/organization/photo/<key>")
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
