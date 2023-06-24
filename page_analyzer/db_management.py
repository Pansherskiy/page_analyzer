from page_analyzer.setting import DATABASE_URL
import psycopg2


CREATE_URLS_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS urls (
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  name VARCHAR(255) UNIQUE NOT NULL,
  created_at DATE NOT NULL
);"""

CREATE_URLS_CHECK_TABLE_QUERY = """
CREATE TABLE IF NOT EXISTS url_checks(
  id bigint PRIMARY KEY GENERATED ALWAYS AS IDENTITY,
  url_id bigint NOT NULL REFERENCES urls (id) ON DELETE CASCADE,
  status_code INT,
  h1 VARCHAR(255),
  title VARCHAR(255),
  description TEXT,
  created_at DATE NOT NULL
);"""


def db_connect():
    try:
        with psycopg2.connect(DATABASE_URL) as conn:
            return conn
    except Exception as error:
        print('Error in db_connect() function!\n', error)


def db_select_query(db_conn, query):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(query)
            tuples_list = cursor.fetchall()
            db_conn.commit()
            return tuple_normalization(tuples_list)
    except Exception as error:
        print('Error in db_select_query() function!\n', error)


def db_query(db_conn, query):
    try:
        with db_conn.cursor() as cursor:
            cursor.execute(query)
            db_conn.commit()
    except Exception as error:
        print('Error in db_query() function!\n', error)


def create_tables(db_conn):
    try:
        db_query(db_conn, CREATE_URLS_TABLE_QUERY)
        db_query(db_conn, CREATE_URLS_CHECK_TABLE_QUERY)
    except Exception as error:
        print('Error in create_urls_table() function!\n', error)


def tuple_normalization(tup):
    if len(tup) == 1 and len(tup[0]) == 1:
        return tup[0][0]
    elif len(tup[0]) == 1:
        return [elem[0] for elem in tup]
    else:
        return tup
