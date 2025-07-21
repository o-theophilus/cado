from flask import Blueprint
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)


user = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'anonymous' NOT NULL,

    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,

    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(100),

    password VARCHAR(200) NOT NULL,
    photo VARCHAR(50),

    access TEXT[] DEFAULT ARRAY[]::TEXT[],
    login BOOLEAN DEFAULT FALSE
);"""


organization = """CREATE TABLE IF NOT EXISTS organization (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'live' NOT NULL,

    slug VARCHAR(255) UNIQUE NOT NULL,
    user_key CHAR(32) NOT NULL,

    name VARCHAR(100) NOT NULL,
    fullname TEXT,
    slogan TEXT,
    about TEXT,
    email_domains TEXT[] DEFAULT ARRAY[]::TEXT[],

    phone VARCHAR(100),
    email VARCHAR(255),
    website VARCHAR(100),
    address JSONB DEFAULT '[]'::JSONB,
    social_links JSONB DEFAULT '{}'::JSONB,

    photo VARCHAR(50),

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE
);"""


# TODO: add manager_card_key CHAR(32) NOT NULL,
card = """CREATE TABLE IF NOT EXISTS card (
    key CHAR(10) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'draft' NOT NULL,

    user_key CHAR(32) NOT NULL,
    organization_key CHAR(32),

    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    job_title VARCHAR(100),
    about TEXT,

    email VARCHAR(255),
    phone VARCHAR(100),
    office_location_id INTEGER DEFAULT 0,
    social_links JSONB DEFAULT '{}'::JSONB,

    photo VARCHAR(50),

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE,
    FOREIGN KEY (organization_key) REFERENCES organization(key)
        ON DELETE SET NULL
);"""


card_organization = """CREATE TABLE IF NOT EXISTS card_organization (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'pending' NOT NULL,

    card_key CHAR(10) UNIQUE NOT NULL,
    organization_key CHAR(32) NOT NULL,

    FOREIGN KEY (card_key) REFERENCES card(key) ON DELETE CASCADE,
    FOREIGN KEY (organization_key) REFERENCES
        organization(key) ON DELETE CASCADE
);"""


code = """CREATE TABLE IF NOT EXISTS code (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,

    user_key CHAR(32) NOT NULL,
    code VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,

    FOREIGN KEY (user_key) REFERENCES "user"(key) ON DELETE CASCADE
);"""

log = """CREATE TABLE IF NOT EXISTS log (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,
    user_key CHAR(32) NOT NULL,
    action VARCHAR(20) NOT NULL,
    entity_key TEXT,
    entity_type VARCHAR(100) NOT NULL,
    status INT DEFAULT 200,
    misc JSONB DEFAULT '{}'::JSONB,

    FOREIGN KEY (user_key) REFERENCES "user"(key)
);"""


def db_open():
    con = psycopg2.connect(os.environ["DATABASE_URI"])
    cur = con.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    return con, cur


def db_close(con, cur):
    con.commit()
    cur.close()
    con.close()
