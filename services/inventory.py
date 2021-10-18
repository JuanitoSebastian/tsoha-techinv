from db import db
from services.users import user_id
from exceptions import UserAuthorityError

def get_inventory_for_device(id):
  sql = "SELECT id, serialnum FROM inventory WHERE model_id=:id"
  result = db.session.execute(sql, {"id" : id})
  return result.fetchall()

def insert_entry_for_device(model_id, serialnum):
  if user_id() == 0:
    raise UserAuthorityError("User not logged in")

  sql = "INSERT INTO inventory (model_id, serialnum) VALUES (:model_id, :serialnum) RETURNING id"
  result = db.session.execute(sql, {"model_id" : model_id, "serialnum" : serialnum })
  inventory_id = result.fetchone()[0]
  sql = "INSERT INTO userinventory (user_id, inventory_id) VALUES (:user_id, :inventory_id)"
  db.session.execute(sql, { "user_id": user_id(), "inventory_id": inventory_id})
  db.session.commit()

# Returns 0 if available, 1 if not available, 2 if reserved for this produciton already
def check_availability(inventory_id, production):
  sql = "SELECT COUNT(*) FROM reservations WHERE inventory_id=:inventory_id AND production_id=:production_id"
  result = db.session.execute(sql, { "inventory_id": inventory_id, "production_id": production.id })
  count = result.fetchone()[0]
  if count != 0: return 2

  sql = "SELECT COUNT(*) FROM reservations, productions WHERE reservations.inventory_id=:inventory_id AND productions.id=reservations.production_id AND (:starting_date <= productions.ending) AND (productions.starting <= :ending_date)"
  result = db.session.execute(sql, { "inventory_id": inventory_id, "starting_date": production.starting, "ending_date": production.ending })
  count = result.fetchone()[0]
  return 0 if count == 0 else 1