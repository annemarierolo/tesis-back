
from api.models import Term
from sqlite3 import Error
from api.services.connection import create_connection
import sqlite3
import json

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

def obtener_trabajos_by_term(id):
    lista = {'propuestas':[], 'tgs':[], 'defensas':[]}
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()

    sql = '''
            select distinct p.titulo, p.id
            from api_term t, api_propuesta p
            where t.id = {0} and t.id = p.fk_term_id 
        '''.format(id)
    cur.execute(sql)
 
    rows = cur.fetchall()

    for row in rows:
        trabajo = {
            'titulo': row[0],
            'id': row[1]
        }
        lista['propuestas'].append(trabajo)
    
    sql = '''
            select distinct p.titulo, tg.id
            from api_term t, api_propuesta p, api_trabajodegrado tg
            where t.id = {0} and t.id = p.fk_term_id and tg.fk_propuesta_id = p.id
        '''.format(id)
    cur.execute(sql)
 
    rows = cur.fetchall()

    for row in rows:
        trabajo = {
            'titulo': row[0],
            'id': row[1]
        }
        lista['tgs'].append(trabajo)

    
    sql = '''
            select distinct p.titulo, p.id
            from api_term t, api_propuesta p, api_trabajodegrado tg, api_defensa d
            where t.id = {0} and t.id = p.fk_term_id and tg.fk_propuesta_id = p.id and tg.id = d.fk_trabajo_grado_id
        '''.format(id)
    cur.execute(sql)
 
    rows = cur.fetchall()

    for row in rows:
        trabajo = {
            'titulo': row[0],
            'id': row[1]
        }
        lista['defensas'].append(trabajo)
    
    return lista

def estadiaticas_by_term(id):

    lista = {'estadisticas':[]}
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()

    sql = "select avg(d.calificacion) as Promedio  from api_term as t, api_defensa as d, api_trabajodegrado as tg  where t.id={0} and t.id = tg.fk_term_id and tg.id = d.fk_trabajo_grado_id".format(id)
    cur.execute(sql)
    row = list(cur.fetchall()[0])
    media_aritmetica = row[0]

    sql = "SELECT (max(d.calificacion)+min(d.calificacion))/2 as mediana from api_term as t, api_defensa as d, api_trabajodegrado as tg  where t.id={0} and t.id = tg.fk_term_id and tg.id = d.fk_trabajo_grado_id".format(id)
    cur.execute(sql)
    row = list(cur.fetchall()[0])
    mediana = row[0]

    sql = "SELECT (AVG(d.calificacion*d.calificacion) - AVG(d.calificacion)*AVG(d.calificacion))/2 FROM api_defensa as d, api_trabajodegrado as tg, api_term as t where t.id={0} and t.id=tg.fk_term_id and tg.id=d.fk_trabajo_grado_id".format(id)
    cur.execute(sql)
    row = list(cur.fetchall()[0])
    desviacion_estandar = row[0]

    sql = '''
            SELECT d.calificacion, COUNT(d.calificacion) as Veces 
            from api_defensa as d, api_trabajodegrado as tg, api_term as t 
            where t.id={0} and t.id=tg.fk_term_id and tg.id=d.fk_trabajo_grado_id
            group by d.calificacion
            ORDER by COUNT(d.calificacion) DESC
            LIMIT 1    
        '''.format(id)
    cur.execute(sql)
    row = list(cur.fetchall()[0])
    moda = row[0]

    obj = {
            'media_aritmetica': media_aritmetica,
            'mediana': mediana,
            'moda': moda,
            'desviacion_estandar': desviacion_estandar
        }
    
    lista['estadisticas'].append(obj)

    return lista


def crear_term(value):
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()
    sql = "INSERT INTO api_term(term) VALUES ('{}')".format(value)
    cur.execute(sql)
    conn.commit()

def actualizar_term(data):
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()
    sql = "UPDATE api_term SET term='{0}' WHERE id={1}".format(data['term'], data['id'])
    cur.execute(sql)
    conn.commit()

def eliminar_term(id):
    conn = create_connection('db.sqlite3')
    cur = conn.cursor()
    sql = "DELETE FROM api_term WHERE id={0}".format(id)
    cur.execute(sql)
    conn.commit()
