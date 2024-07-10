from flask import Blueprint, jsonify, request
import re
import os
from .tools import send_mail
from .postgres import db_open, db_close
from .postgres import user_table, code_table


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


# @bp.get("/fix")
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
        RENAME COLUMN organization
        TO organization_key;
    """)

    db_close(con, cur)
    return jsonify({
        "status": 200
    })
