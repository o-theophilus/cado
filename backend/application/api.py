from flask import Blueprint, jsonify
from .postgres import db_open, db_close
from .postgres import user_table, code_table
from .admin import access
import os

bp = Blueprint("api", __name__)


def create_tables():
    con, cur = db_open()

    cur.execute(f"""
        DROP TABLE IF EXISTS "user" CASCADE;
        DROP TABLE IF EXISTS code CASCADE;
        {user_table}
        {code_table}
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


def general_fix():
    con, cur = db_open()

    # cur.execute("""
    #     ALTER TABLE item
    #     RENAME COLUMN old_price
    #     TO discount_time;

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     TYPE VARCHAR(32);

    #     ALTER TABLE item
    #     ALTER COLUMN discount_time
    #     SET DEFAULT 'TRUE';

    #     UPDATE item
    #     SET discount_time = 'TRUE';

    # ALTER TABLE post
    # DROP COLUMN videos;

    #     ALTER TABLE order_item
    #     ADD COLUMN price FLOAT DEFAULT 0 NOT NULL;
    # """)

    cur.execute("""
        ALTER TABLE "user"
        DROP COLUMN admin;
    """)
    cur.execute("""
        ALTER TABLE "user"
        ADD COLUMN access TEXT[] DEFAULT ARRAY[]::TEXT[];
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })


# @bp.get("/fix")
def fix_permission():
    con, cur = db_open()

    cur.execute("""
            UPDATE "user"
            SET access = %s
            WHERE email = %s;
        """, (
        [f"{x}:{y[0]}" for x in access for y in access[x]],
        os.environ["MAIL_USERNAME"]
    ))

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
