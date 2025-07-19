from flask import Blueprint, jsonify, request
from .postgres import db_open, db_close
from .tools import token_to_user
from .card_get import get as get_card, get_org_cards
from uuid import uuid4


bp = Blueprint("org_card", __name__)


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

    cards = get_org_cards(org["key"], cur)
    db_close(con, cur)
    return cards
