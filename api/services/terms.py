from sqlite_orm.database import Database
from api.models import Term
import sqlite3
from sqlite3 import Error
import json
from api.services.connection import create_connection

def obtener_terms():
    lista = {'terms':[]}
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()
    """ cur.execute("INSERT INTO api_term(term) VALUES ('2221')")
    conn.commit() """
    cur.execute("SELECT * FROM api_term")
 
    rows = cur.fetchall()

    for row in rows:
        term = {
            'id': row[0],
            'term': row[1]
        }
        lista['terms'].append(term)
    return lista

""" def crear_term(): """

