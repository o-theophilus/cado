from flask import Blueprint, jsonify
from .postgres import db_open, db_close
from .postgres import user, code, organization, user_organization
from .admin import clean_photo

bp = Blueprint("api", __name__)


# TODO: test this
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
        DROP TABLE IF EXISTS user_organization CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        {user}
        {organization}
        {user_organization}
        {code}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


@bp.get("/fix")
def fix():
    con, cur = db_open()

    # cur.execute(f"""
    #     {user_organization}
    # """)

    # cur.execute("""
    #     ALTER TABLE "user"
    #     DROP COLUMN organization_key;
    # """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
