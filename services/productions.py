from db import db

def get_all_productions():
  sql = "SELECT id, name, starting, ending FROM productions"
  result = db.session.execute(sql)
  return result.fetchall()

def insert_production(name, starting, ending):
  sql = "INSERT INTO productions (name, starting, ending) VALUES (:name, :starting, :ending)"
  db.session.execute(sql, { "name":name, "starting":starting, "ending":ending })
  db.session.commit()

def get_production(production_id):
  sql = "SELECT id, name, starting, ending FROM productions WHERE id=:production_id"
  result = db.session.execute(sql, { "production_id":production_id })
  return result.fetchone()
