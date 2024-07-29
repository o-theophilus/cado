from flask import Blueprint, jsonify
from .postgres import db_open, db_close
from .postgres import user_table, code_table, organization_table
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
        DROP TABLE IF EXISTS code CASCADE;
        {user_table}
        {organization_table}
        {code_table}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
