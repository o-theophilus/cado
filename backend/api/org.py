from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user, org_schema, reserved_words
import re
from uuid import uuid4
from psycopg2.extras import Json
from werkzeug.security import check_password_hash
from math import ceil

bp = Blueprint("org", __name__)


@bp.post("/org")
def create():
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
        or "name" not in request.json
        or not request.json["name"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "name": "this field is required"
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
                key, slug, name, fullname, email, user_key
            )
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING *;
        """, (
        uuid4().hex,
        slug,
        request.json["name"].strip(),
        request.json["name"].strip(),
        user["email"],
        user["key"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "org": org_schema(org),
    })


@bp.put("/org/<key>")
def update(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM organization WHERE key = %s AND user_key = %s;",
                (key, user["key"]))
    org = cur.fetchone()
    if not org or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}

    if "name" in request.json:
        if not request.json["name"]:
            error['name'] = "this field is required"
        org["name"] = request.json["name"].strip()

    if "fullname" in request.json:
        org["fullname"] = request.json["fullname"]

    if "slogan" in request.json:
        org["slogan"] = request.json["slogan"]

    if "about" in request.json:
        org["about"] = request.json["about"]

    if "phone" in request.json:
        phone = request.json["phone"]
        if phone:
            phone = phone.replace(' ', '')
            if not re.match(r'^\+?\d+$', phone):
                error['phone'] = """Invalid phone number. Phone number may
                    start with a '+' followed by digits"""
        org["phone"] = phone

    if "website" in request.json:
        org["website"] = request.json["website"]

    if "email_domains" in request.json:
        if type(request.json["email_domains"]) is not list:
            error['email_domains'] = "invalid request"
        else:
            bad = [x for x in request.json["email_domains"]
                   if not re.match(r"^@\w+\.\w+$", x)]
            if bad != []:
                error['email_domains'] = f"""invalid format: {", ".join(bad)}.
                    Each domain must start with '@', contain no spaces, and be
                    in the format '@domain.tld'."""
        org["email_domains"] = request.json["email_domains"]

    if "address" in request.json:
        if type(request.json["address"]) is not list:
            error['address'] = "invalid request"
        org["address"] = request.json["address"]

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
        org["social_links"] = links

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE organization
        SET
            name = %s,
            fullname = %s,
            slogan = %s,
            about = %s,
            email_domains = %s,
            phone = %s,
            website = %s,
            address = %s,
            social_links = %s
        WHERE key = %s
        RETURNING *;
    """, (
        org["name"],
        org["fullname"],
        org["slogan"],
        org["about"],
        org["email_domains"],
        org["phone"],
        org["website"],
        Json(org["address"]),
        Json(org["social_links"]),
        org["key"]
    ))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "org": org_schema(org)
    })


@bp.post("/org/slug/1/<key>")
def slug_check(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM organization WHERE key = %s AND user_key = %s;",
                (key, user["key"]))
    org = cur.fetchone()

    if not org or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = None
    if "slug" not in request.json or not request.json["slug"]:
        error = "this field is required"
    elif request.json["slug"] == org["slug"]:
        error = "no change"
    else:
        slug = re.sub('-+', '-', re.sub(
            '[^a-zA-Z0-9]', '-', request.json["slug"].strip().lower()))
        cur.execute("""
            SELECT * FROM organization WHERE key != %s AND slug = %s
        ;""", (org["key"], slug))
        if cur.fetchone() or slug in reserved_words:
            error = "not available"

    if error:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "slug": error
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "org": org_schema(org)
    })


@bp.post("/org/slug/2/<key>")
def slug(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("SELECT * FROM organization WHERE key = %s AND user_key = %s;",
                (key, user["key"]))
    org = cur.fetchone()

    if not org or not request.json:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    error = {}
    if "slug" not in request.json or not request.json["slug"]:
        error["slug"] = "this field is required"
    elif request.json["slug"] == org["slug"]:
        error["slug"] = "no change"
    else:
        slug = re.sub('-+', '-', re.sub(
            '[^a-zA-Z0-9]', '-', request.json["slug"].strip().lower()))
        cur.execute("""
            SELECT * FROM organization WHERE key != %s AND slug = %s;
        """, (org["key"], slug))
        if cur.fetchone() or slug in reserved_words:
            error["slug"] = "not available"

    if "password" not in request.json or not request.json["password"]:
        error["password"] = "this field is required"
    elif not check_password_hash(user["password"], request.json["password"]):
        error["password"] = "incorrect password"

    if error != {}:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            **error
        })

    cur.execute("""
        UPDATE organization SET slug = %s WHERE key = %s RETURNING *;
    """, (slug, org["key"]))
    org = cur.fetchone()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "org": org_schema(org)
    })


@bp.get("/org/<key>")
def get(key):
    con, cur = db_open()

    cur.execute("""
        SELECT * FROM organization WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()

    if not org:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "not found"
        })

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "org": org_schema(org)
    })


@bp.get("/org")
def get_many():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order_by = {
        'name (a-z)': 'name',
        'name (z-a)': 'name'
    }

    order_dir = {
        'name (a-z)': 'ASC',
        'name (z-a)': 'DESC'
    }

    order = list(order_by.keys())[0]
    status = "live"
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
        FROM organization
        WHERE
            (
                %s = '' OR status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', key, name, email
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
    orgs = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "orgs": [org_schema(x) for x in orgs],
        "order_by": list(order_by.keys()),
        "_status": ['live', 'draft'],
        "total_page": ceil(orgs[0]["_count"] / page_size) if orgs else 0
    })
