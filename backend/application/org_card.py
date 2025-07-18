from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user, card_schema
from .card_get import get as get_card
from uuid import uuid4
from math import ceil


bp = Blueprint("org_card", __name__)


@bp.get("/org/card/<key>")
def get_org_card(key, cur=None):

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
        "_status": ['pending', 'live'],
        "total_page": ceil(cards[0]["_count"] / page_size) if cards else 0
    })


@bp.post("/org/card/join/<key>")
def join(key):
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
        or "org_key" not in request.json
        or not request.json["org_key"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM organization WHERE key = %s;
    """, (request.json["org_key"],))
    org = cur.fetchone()

    cur.execute("""
        SELECT * FROM card WHERE key = %s;
    """, (key,))
    card = cur.fetchone()

    if not org or not card or user["key"] != card["user_key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    if org["email_domains"] != []:
        domain = None
        if card["email"]:
            domain = f"@{card["email"].split("@")[1]}"

        if not domain or domain not in org["email_domains"]:
            db_close(con, cur)
            return jsonify({
                "status": 400,
                "error": "email not supported" if card["email"] else "no email"
            })

    cur.execute("""
        DELETE FROM card_organization WHERE card_key = %s
    ;""", (card["key"],))

    cur.execute("""
        INSERT INTO card_organization (
            key, status, card_key, organization_key)
        VALUES (%s, %s, %s, %s);
    """, (
        uuid4().hex,
        "pending",
        card["key"],
        org["key"]
    ))

    cur.execute("""
        UPDATE card SET status = %s, organization_key = %s
        WHERE key = %s;
    """, ("pending", org["key"], card["key"]))

    card = get_card(card["key"], cur).json
    if card and "card" in card:
        card = card["card"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card
    })


@bp.delete("/org/card/cancel/<key>")
def owner_cancel(key):
    con, cur = db_open()

    user = token_to_user(cur)
    if not user:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid token"
        })

    cur.execute("""
        SELECT * FROM card WHERE key = %s;
    """, (key,))
    card = cur.fetchone()
    if not card:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM organization WHERE key = %s;
    """, (card["organization_key"],))
    org = cur.fetchone()

    if (
        not card
        or not org
        or user["key"] not in [org["user_key"], card["user_key"]]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        UPDATE card
        SET status = %s,
        organization_key = NULL,
        office_location_id = 0
        WHERE key = %s;
    """, ('draft', card["key"]))

    cur.execute("""
        DELETE FROM card_organization WHERE card_key = %s
    ;""", (card["key"],))

    card = get_card(card["key"], cur).json
    if card and "card" in card:
        card = card["card"]

    db_close(con, cur)
    return jsonify({
        "status": 200,
        "card": card
    })


@bp.post("/org/card/status/<key>")
def status(key):
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
        or "card_keys" not in request.json
        or not request.json["card_keys"]
        or type(request.json["card_keys"]) is not list
        or "status" not in request.json
        or not request.json["status"]
        or request.json["status"] not in ["live", "draft"]
    ):
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    cur.execute("""
        SELECT * FROM organization WHERE key = %s;
    """, (key,))
    org = cur.fetchone()

    if not org or user["key"] != org["user_key"]:
        db_close(con, cur)
        return jsonify({
            "status": 400,
            "error": "invalid request"
        })

    status_filter = ""
    if request.json["status"] == "live":
        status_filter = "AND status = 'pending'"
    elif request.json["status"] == "draft":
        status_filter = "AND status IN ['pending', 'live']"

    print(request.json["card_keys"])
    cards = []
    if status_filter:
        cur.execute("""
            SELECT * FROM card
            WHERE
                key = ANY(%s)
                AND organization_key = %s
                AND status = ANY(%s)
        ;""", (
            request.json["card_keys"],
            org["key"],
            ['pending'] if request.json["status"] == "live" else [
                'pending', 'live']
        ))
        cards = cur.fetchall()

    bad = []
    card_keys = []
    if request.json["status"] == "live" and org["email_domains"] != []:
        for card in cards:
            domain = None
            if card["email"]:
                domain = f"@{card["email"].split("@")[1]}"

            if not domain or domain not in org["email_domains"]:
                bad.append(card)
            else:
                card_keys.append(card["key"])
    else:
        card_keys = [x["key"] for x in cards]

    cur.execute("""
        UPDATE card
        SET status = %s,
        organization_key = %s,
        office_location_id = 0
        WHERE key = ANY(%s)
    ;""", (
        request.json["status"],
        org["key"] if request.json["status"] == "live" else None,
        card_keys
    ))

    cur.execute("""
        DELETE FROM card_organization WHERE card_key = ANY(%s)
    ;""", (card_keys,))

    cards = get_org_card(org["key"], cur)
    db_close(con, cur)
    return cards
