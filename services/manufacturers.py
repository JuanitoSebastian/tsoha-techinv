from db import db
from services.users import user_id
import exceptions

def get_all_manufacturers():
  sql = "SELECT id, name FROM manufacturers"
  results = db.session.execute(sql)
  return results.fetchall()

def insert_manufacturer(name):
  if user_id() == 0:
    raise exceptions.UserAuthorityError("User not logged in")

  sql = "INSERT INTO manufacturers (name) VALUES (:name) RETURNING id"
  result = db.session.execute(sql, { "name" : name })
  manufacturer_id = result.fetchone()[0]
  sql = "INSERT INTO usermanufacturers (user_id, manufacturer_id) VALUES (:user_id, :manufacturer_id)"
  db.session.execute(sql, { "user_id": user_id(), "manufacturer_id": manufacturer_id })
  db.session.commit()

  return True