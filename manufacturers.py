from db import db

def get_list():
  sql = "SELECT id, name FROM manufacturers"
  results = db.session.execute(sql)
  return results.fetchall()

def insert_manufacturer(name):
  sql = "INSERT INTO manufacturers (name) VALUES (:name)"
  db.session.execute(sql, { "name" : name })
  db.session.commit()