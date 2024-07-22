from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema,  token_tool, reserved_words)
from uuid import uuid4
import re
from werkzeug.security import generate_password_hash, check_password_hash
from .storage import storage
import json


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
    if (
        not org
        or (
            "email_domains" in request.json
            and type(request.json["email_domains"]) is not list)
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "name" not in request.json or not request.json["name"]:
        error["name"] = "this field is required"

    for x in request.json["email_domains"]:
        x = x.strip()
        if not re.match(r"\@\S+\.\S+", x):
            if "email_domains" not in error:
                error["email_domains"] = f"invalid domain: {x}"
            else:
                error["email_domains"] = f"{error['email_domains']}, {x}"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

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

    fullname = None
    slogan = None
    if "fullname" in request.json and request.json["fullname"]:
        fullname = request.json["fullname"]
    if "slogan" in request.json and request.json["slogan"]:
        slogan = request.json["slogan"]

    cur.execute("""
        UPDATE organization
        SET
            slug = %s,
            name = %s,
            fullname = %s,
            slogan = %s,
            email_domains = %s
        WHERE key = %s
        RETURNING *;
    """, (
        slug,
        request.json["name"],
        fullname,
        slogan,
        request.json["email_domains"],
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

    error = {}

    if "email" not in request.json or not request.json["email"]:
        error["email"] = "this field is required"
    elif not re.match(r"\S+@\S+\.\S+", request.json["email"]):
        error["email"] = "invalid email"
    if "email" not in error:
        cur.execute(
            'SELECT * FROM organization WHERE key != %s AND email = %s;', (
                org["key"], request.json["email"]
            )
        )
        if cur.fetchone():
            error["email"] = "email taken"
    if (
        "email" not in error
        and org["email_domains"] != []
        and not request.json["email"].endswith(tuple(org["email_domains"]))
    ):
        error = "invalid email domain"

    id = 0
    for x in request.json["address"]:
        if "name" not in x or not x["name"]:
            if f"{id}" not in error:
                error[f"{id}"] = {}
            error[f"{id}"]["name"] = "this field is required"
        if "address" not in x or not x["address"]:
            if f"{id}" not in error:
                error[f"{id}"] = {}
            error[f"{id}"]["address"] = "this field is required"
        id += 1

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
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
            address = %s::JSONB[]
        WHERE key = %s
        RETURNING *;
    """, (
        phone,
        request.json["email"],
        website,
        [json.dumps(x) for x in request.json["address"]],
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


@ bp.put("/organization/<key>/<_type>")
def add_photo(key, _type):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if f"organization:edit_{_type}" not in user["access"]:
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

    if org[_type]:
        storage(org[_type], delete=True)

    file_name = storage(file)

    cur.execute("""
        UPDATE organization
        SET {} = %s
        WHERE key = %s
        RETURNING *;
    """.format(_type), (
        file_name,
        org["key"]
    ))
    org = cur.fetchone()

    if org["logo"]:
        org["logo"] = f"{request.host_url}photo/{org['logo']}"
    if org["icon"]:
        org["icon"] = f"{request.host_url}photo/{org['icon']}"

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "organization": org
    })


@ bp.delete("/organization/<key>/<_type>")
def delete_photo(key, _type):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if f"organization:edit_{_type}" not in user["access"]:
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

    if org[_type]:
        storage(org[_type].split("/")[-1], delete=True)

        cur.execute("""
            UPDATE organization
            SET {} = NULL
            WHERE key = %s;
        """.format(_type), (
            user["key"],
        ))

    db_close(con, cur)
    return jsonify({
        "status": 200
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
