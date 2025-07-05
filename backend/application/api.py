from flask import Blueprint, jsonify
from .postgres import db_open, db_close
from .postgres import user, card, organization, card_organization, code
from .admin import clean_photo

bp = Blueprint("api", __name__)


# TODO: test this
@bp.get("/cron")
def cron():
    clean_photo()
    return jsonify({
        "status": 200
    })


# @bp.get("/fix")
def create_tables():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS organization CASCADE;
        DROP TABLE IF EXISTS card CASCADE;
        DROP TABLE IF EXISTS card_organization CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        {user}
        {organization}
        {card}
        {card_organization}
        {code}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE organization
        RENAME COLUMN logo TO photo;
        ALTER TABLE organization
        DROP COLUMN IF EXISTS icon;
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
