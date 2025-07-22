from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import (
    token_to_user, user_schema, org_schema, card_schema, send_mail,
    generate_code, check_code)
import re
from uuid import uuid4
from psycopg2.extras import Json
from werkzeug.security import check_password_hash
from .storage import storage
from .card_get import get as get_card
from .log import log


bp = Blueprint("card", __name__)


@bp.post("/card")
def create():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    if not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "firstname" not in request.json or not request.json["firstname"]:
        error["firstname"] = "this field is required"
    if "lastname" not in request.json or not request.json["lastname"]:
        error["lastname"] = "this field is required"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    job_title = None
    if "job_title" in request.json and request.json["job_title"]:
        job_title = request.json["job_title"]

    cur.execute("""
        INSERT INTO card (
            key, firstname, lastname, job_title,
            email, phone, photo, user_key
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING *;
    """, (
        uuid4().hex[:10],
        request.json["firstname"].strip(),
        request.json["lastname"].strip(),
        job_title,
        user["email"],
        user["phone"],
        user["photo"],
        user["key"]
    ))
    card = cur.fetchone()

    log(
        cur=cur,
        user_key=user["key"],
        action="created",
        entity_key=card["key"] if card else None,
        entity_type="card"
    )

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card_schema(card),
    })


@bp.put("/card/<key>")
def update(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM card WHERE key = %s AND user_key = %s;",
                (key, user["key"]))
    card = cur.fetchone()
    if not card or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "firstname" in request.json:
        if not request.json["firstname"]:
            error['firstname'] = "this field is required"
        card["firstname"] = request.json["firstname"].strip()

    if "lastname" in request.json:
        if not request.json["lastname"]:
            error['lastname'] = "this field is required"
        card["lastname"] = request.json["lastname"].strip()

    if "job_title" in request.json:
        card["job_title"] = request.json["job_title"]

    if "about" in request.json:
        card["about"] = request.json["about"]

    if "phone" in request.json:
        phone = request.json["phone"]
        if phone:
            phone = phone.replace(' ', '')
            if not re.match(r'^\+?\d+$', phone):
                error['phone'] = """Invalid phone number. Phone number may
                    start with a '+' followed by digits"""
        card["phone"] = phone

    if "manager_card_key" in request.json:
        card["manager_card_key"] = request.json["manager_card_key"]

    if "office_location_id" in request.json:
        if type(request.json["office_location_id"]) is not int:
            error['social_links'] = "invalid request"
        card["office_location_id"] = request.json["office_location_id"]

    if "social_links" in request.json:
        links = request.json["social_links"]
        if type(request.json["social_links"]) is not dict:
            error['social_links'] = "invalid request"
        else:
            links = {k: v for k,
                     v in request.json["social_links"].items() if k and v}
            if "whatsapp" in links:
                links["whatsapp"] = links["whatsapp"].replace(' ', '')
                if not re.match(r'^\+\d{1,3}\d*$', links["whatsapp"]):
                    error['whatsapp'] = """
                        Invalid phone number. Phone number should start with a
                        "+" followed by the country code and then the phone
                        number. For example, +2348012345678."""
        card["social_links"] = links

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE card
        SET
            firstname = %s,
            lastname = %s,
            job_title = %s,
            about = %s,
            phone = %s,
            manager_card_key = %s,
            office_location_id = %s,
            social_links = %s
        WHERE key = %s
    ;""", (
        card["firstname"],
        card["lastname"],
        card["job_title"],
        card["about"],
        card["phone"],
        card["manager_card_key"],
        card["office_location_id"],
        Json(card["social_links"]),
        card["key"]
    ))

    card = get_card(card["key"], cur).json
    if card and "card" in card:
        card = card["card"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card
    })


# common #############################################################


@bp.delete("/delete/<_type>/<key>")
def delete(key, _type):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute(f"""
        SELECT * FROM {"organization" if _type == "org" else _type}
        WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    if not cur.fetchone() or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "password" not in request.json or not request.json["password"]:
        error = "this field is required"
    elif not check_password_hash(user["password"], request.json["password"]):
        error = "incorrect password"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "password": error
        })

    cur.execute(f"""
        DELETE FROM {"organization" if _type == "org" else _type}
        WHERE key = %s AND user_key = %s
    ;""", (key,))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/email/1/<_type>/<key>")
def email_request_code(key, _type):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute(f"""
        SELECT * FROM {"organization" if _type == "org" else _type}
        WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    entity = cur.fetchone()

    if (
        not entity
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
    elif request.json["email"] == entity["email"]:
        error = "please use a different email form your current email"
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "email": error
        })

    send_mail(
        request.json["email"],
        "New Email Verification Code",
        request.json['email_template'].format(
            firstname=user["firstname"],
            code=generate_code(
                cur,
                user["key"],
                request.json["email"]
            )
        )
    )

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.post("/email/2/<_type>/<key>")
def email(key, _type):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute(f"""
        SELECT * FROM {"organization" if _type == "org" else _type}
        WHERE key = %s AND user_key = %s;
    """, (key, user["key"]))
    entity = cur.fetchone()
    if not entity or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = check_code(cur, user["key"], request.json["email"])
    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute(f"""
        UPDATE {"organization" if _type == "org" else _type}
        SET email = %s WHERE key = %s RETURNING *;
    """, (request.json["email"], entity["key"]))
    entity = cur.fetchone()

    cur.execute("DELETE FROM code WHERE user_key = %s;", (user["key"],))

    if _type == "org":
        entity = org_schema(entity)
    elif _type == "card":
        entity = card_schema(entity)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        _type: entity
    })


@bp.post("/photo/<_type>/<key>/<name>")
def add_photo(_type, key, name):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute(f"""
        SELECT * FROM {"organization" if _type == "org" else _type}
        WHERE key = %s OR user_key = %s;
    """, (key, user["key"]))
    entity = cur.fetchone()

    if not entity or user['key'] not in [entity['key'], entity['user_key']]:
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

    if entity[name]:
        storage("delete", entity[name])

    file_name = storage("save", file)

    cur.execute(f"""
        UPDATE {"organization" if _type == "org" else _type}
        SET {name} = %s WHERE key = %s RETURNING *;
    """, (file_name, entity["key"]))
    entity = cur.fetchone()

    if _type == "org":
        entity = org_schema(entity)
    elif _type == "card":
        entity = card_schema(entity)
    elif _type == "user":
        entity = user_schema(entity)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        _type: entity
    })


@bp.delete("/photo/<_type>/<key>/<name>")
def delete_photo(_type, key, name):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute(f"""
        SELECT * FROM {"organization" if _type == "org" else _type}
        WHERE key = %s;
    """, (key,))
    entity = cur.fetchone()

    if not entity or user['key'] not in [entity['key'], entity['user_key']]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if entity[name]:
        storage("delete", entity[name].split("/")[-1])

        cur.execute(f"""
            UPDATE {"organization" if _type == "org" else _type}
            SET {name} = NULL WHERE key = %s RETURNING *
        ;""", (entity["key"],))
        entity = cur.fetchone()

    if _type == "org":
        entity = org_schema(entity)
    elif _type == "card":
        entity = card_schema(entity)
    elif _type == "user":
        entity = user_schema(entity)

    db_close(con, cur)
    return jsonify({
        "status": 200,
        _type: entity
    })
