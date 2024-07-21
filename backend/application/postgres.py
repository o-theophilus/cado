from flask import Blueprint
import os
import psycopg2
import psycopg2.extras


bp = Blueprint("postgres", __name__)


user_table = """CREATE TABLE IF NOT EXISTS "user" (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'anonymous' NOT NULL,

    slug VARCHAR(255) UNIQUE NOT NULL,

    firstname VARCHAR(100) NOT NULL,
    lastname VARCHAR(100) NOT NULL,
    about_me TEXT,

    role VARCHAR(100),
    organization_key VARCHAR(255),
    manager_email VARCHAR(255),

    email VARCHAR(255) UNIQUE NOT NULL,
    phone VARCHAR(100),
    office_location VARCHAR(255),

    whatsapp VARCHAR(100),
    linkedin VARCHAR(100),
    facebook VARCHAR(100),
    twitter VARCHAR(100),
    instagram VARCHAR(100),

    password VARCHAR(200) NOT NULL,
    photo VARCHAR(50),

    access TEXT[] DEFAULT ARRAY[]::TEXT[],
    login BOOLEAN DEFAULT FALSE
);"""

organization_table = """CREATE TABLE IF NOT EXISTS organization (
    key CHAR(32) PRIMARY KEY,
    status VARCHAR(20) DEFAULT 'live' NOT NULL,

    slug VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(100) NOT NULL,
    fullname TEXT,
    slogan TEXT,

    phone VARCHAR(100),
    email VARCHAR(255) UNIQUE NOT NULL,
    website VARCHAR(100),
    address JSONB[] DEFAULT ARRAY[]::JSONB[],

    whatsapp VARCHAR(100),
    linkedin VARCHAR(100),
    facebook VARCHAR(100),
    twitter VARCHAR(100),
    instagram VARCHAR(100),

    logo VARCHAR(50),
    icon VARCHAR(50),
    email_domains TEXT[] DEFAULT ARRAY[]::TEXT[]
);"""


code_table = """CREATE TABLE IF NOT EXISTS code (
    key CHAR(32) PRIMARY KEY,
    date TIMESTAMP NOT NULL,

    user_key CHAR(32) NOT NULL,
    code VARCHAR(10) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,

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
