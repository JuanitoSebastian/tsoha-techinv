from db import db
from services.users import user_id
from exceptions import UserAuthorityError

def get_inventory_for_device(id):
  sql = "SELECT id, serialnum, available FROM inventory WHERE model_id=:id"
  result = db.session.execute(sql, {"id" : id})
  return result.fetchall()

def insert_entry_for_device(model_id, serialnum, available):
  if user_id() == 0:
    raise UserAuthorityError("User not logged in")

  sql = "INSERT INTO inventory (model_id, serialnum, available) VALUES (:model_id, :serialnum, :available) RETURNING id"
  result = db.session.execute(sql, {"model_id" : model_id, "serialnum" : serialnum, "available" : available})
  inventory_id = result.fetchone()[0]
  sql = "INSERT INTO userinventory (user_id, inventory_id) VALUES (:user_id, :inventory_id)"
  db.session.execute(sql, { "user_id": user_id(), "inventory_id": inventory_id})
  db.session.commit()

def check_availability(inventory_id, starting_date, ending_date):
  return False