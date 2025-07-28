from flask import Blueprint, request, jsonify
from .tools import token_to_user, card_schema
from math import ceil
from .postgres import db_close, db_open


bp = Blueprint("card_get", __name__)


@bp.get("/card/<key>")
def get(key, cur=None):

    close_conn = not cur
    if not cur:
        con, cur = db_open()

    cur.execute("""
        SELECT
        card.*,
        jsonb_build_object(
            'key', org.key,
            'status', org.status,
            'slug', org.slug,
            'name', org.name,
            'fullname', org.fullname,
            'slogan', org.slogan,
            'about', org.about,
            'email_domains', org.email_domains,
            'phone', org.phone,
            'email', org.email,
            'website', org.website,
            'address', COALESCE(org.address::jsonb, '[]'::jsonb),
            'social_links', org.social_links,
            'photo', org.photo,
            'user_key', org.user_key
        ) AS org

        FROM card
        LEFT JOIN organization AS org
            ON card.organization_key = org.key
        WHERE card.key = %s

        GROUP BY card.key,
        org.key, org.status, org.slug, org.name, org.fullname,
        org.slogan, org.about, org.email_domains, org.phone, org.email,
        org.website, org.address, org.social_links, org.photo
    ;""", (key,))
    card = cur.fetchone()

    if not card:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card_schema(card)
    })


@bp.get("/card")
def get_user_cards():
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    order_by = {
        'name (a-z)': 'card.firstname',
        'name (z-a)': 'card.firstname'
    }

    order_dir = {
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
            card.*,
            COUNT(*) OVER() AS _count,
            jsonb_build_object(
                'key', org.key,
                'status', org.status,
                'slug', org.slug,
                'name', org.name,
                'fullname', org.fullname,
                'slogan', org.slogan,
                'about', org.about,
                'email_domains', org.email_domains,
                'phone', org.phone,
                'email', org.email,
                'website', org.website,
                'address', org.address,
                'social_links', org.social_links,
                'photo', org.photo
            ) AS org

        FROM card
        LEFT JOIN organization AS org ON card.organization_key = org.key
        WHERE
            card.user_key = %s AND
            (
                %s = '' OR card.status = %s
            ) AND (
                %s = ''
                OR CONCAT_WS(', ', card.key, card.firstname, card.lastname,
                card.email
                ) ILIKE %s
            )
        ORDER BY {} {}
        LIMIT %s OFFSET %s;
    """.format(
        order_by[order], order_dir[order]
    ), (
        user["key"],
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    cards = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "cards": [card_schema(x) for x in cards],
        "order_by": list(order_by.keys()),
        "_status": ['live', 'pending'],
        "total_page": ceil(cards[0]["_count"] / page_size) if cards else 0
    })


@bp.get("/org/card/<key>")
def get_org_cards(key, cur=None):

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

    cur.execute("""
        SELECT * FROM organization WHERE slug = %s OR key = %s;
    """, (key, key))
    org = cur.fetchone()

    if not org or user["key"] != org["user_key"]:
        if close_conn:
            db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
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
        SELECT *, COUNT(*) OVER() AS _count
        FROM card
        WHERE (
        organization_key = %s
        ) AND (
            %s = '' OR status = %s
        ) AND (
            %s = ''
            OR CONCAT_WS(', ', key, firstname,
            lastname, email
            ) ILIKE %s
        )

        ORDER BY {} {}
        LIMIT %s OFFSET %s
    ;""".format(
        order_by[order], order_dir[order]
    ), (
        org["key"],
        status, status,
        search, f"%{search}%",
        page_size, (page_no - 1) * page_size
    ))
    cards = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "cards": [card_schema(x) for x in cards],
        "order_by": list(order_by.keys()),
        "_status": ['live', 'pending'],
        "total_page": ceil(cards[0]["_count"] / page_size) if cards else 0
    })


@bp.get("/org/emails/<key>")
def get_org_emails(key):
    con, cur = db_open()

    cur.execute("""
        WITH this_card AS (
            SELECT organization_key
            FROM card
            WHERE key = %s
        )
        SELECT card.key, card.firstname, card.lastname, card.email
        FROM card
        JOIN this_card ON card.organization_key = this_card.organization_key
        WHERE
            card.key != %s
            AND card.status = 'live'
    ;""", (key, key))
    emails = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "emails": emails
    })


@bp.get("/card/chart/<key>")
def chart(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM card WHERE key = %s
    ;""", (key,))
    card = cur.fetchone()

    if not card or card["user_key"] != user["key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    # TODO: uncomment the query below
    cur.execute("""
        SELECT
        date_trunc('day', log.date) AS day,
        COUNT(*) AS count
        FROM log
        WHERE
            entity_key = %s
            AND action = 'viewed'
--         AND user_key != %s
        GROUP BY day
        ORDER BY day ASC
    ;""", (card["key"], user["key"]))
    data = cur.fetchall()

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card_schema(card),
        "data": data
    })
