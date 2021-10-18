from db import db
from services.users import user_id
from exceptions import UserAuthorityError


def get_all_productions():
  sql = "SELECT id, name, starting, ending FROM productions"
  result = db.session.execute(sql)
  return result.fetchall()

def insert_production(name, starting, ending):
  if user_id() == 0:
    raise UserAuthorityError("User not logged in")

  sql = "INSERT INTO productions (name, starting, ending) VALUES (:name, :starting, :ending) RETURNING id"
  result = db.session.execute(sql, { "name":name, "starting":starting, "ending":ending })
  production_id = result.fetchone()[0]
  sql = "INSERT INTO userproductions (user_id, production_id) VALUES (:user_id, :production_id)"
  db.session.execute(sql, { "user_id": user_id(), "production_id": production_id})
  db.session.commit()

def get_production(production_id):
  sql = "SELECT productions.id, productions.name, productions.starting, productions.ending, users.username creator FROM productions, users, userproductions WHERE productions.id=:production_id AND productions.id=userproductions.production_id AND userproductions.user_id=users.id"
  result = db.session.execute(sql, { "production_id": production_id })
  return result.fetchone()

def get_production_name(production_id):
  sql = "SELECT name FROM productions WHERE id=:production_id"
  result = db.session.execute(sql, { "production_id": production_id })
  name = result.fetchone()[0]
  return name
