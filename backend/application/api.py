from flask import Blueprint, jsonify
from .postgres import db_open, db_close
from .postgres import user, card, organization, card_organization, code, log
from .admin import clean_photo
from .tools import token_to_user

bp = Blueprint("api", __name__)


@bp.get("/cron")
def cron():
    clean_photo()
    return jsonify({
        "status": 200
    })


def create_tables():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS organization CASCADE;
        DROP TABLE IF EXISTS card CASCADE;
        DROP TABLE IF EXISTS card_organization CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        DROP TABLE IF EXISTS log CASCADE;
        {user}
        {organization}
        {card}
        {card_organization}
        {code}
        {log}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/fix")
def fix():
    con, cur = db_open()

    cur.execute("""
        ALTER TABLE card
        ADD COLUMN IF NOT EXISTS manager_card_key CHAR(10);
    """)
    cur.execute(log)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/notification")
def notification(cur=None):

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
        SELECT org.slug
        FROM card_organization AS c_org
        LEFT JOIN organization AS org ON c_org.organization_key = org.key
        WHERE org.user_key = %s;
    """, (user["key"],))
    nots = cur.fetchall()

    if close_conn:
        db_close(con, cur)
    return jsonify({
        "status": 200,
        "nots": [
            {
                "_type": 'org_card_join_request',
                "info": {
                    "count": len(nots),
                    "slug": nots[0]["slug"]
                }
            }
        ]
    })
