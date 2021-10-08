from db import db
from exceptions import UserAuthorityError
from services.users import user_id

def get_equipment():
  sql = "SELECT equipment.id, equipment.model, manufacturers.name manufacturer, COALESCE(invcount.count, 0) count FROM (SELECT * FROM equipment WHERE visible=TRUE) AS equipment JOIN manufacturers ON manufacturers.id=equipment.manufacturer_id LEFT JOIN (SELECT model_id, COUNT(model_id) FROM inventory GROUP BY model_id) AS invcount ON invcount.model_id=equipment.id"
  result = db.session.execute(sql)
  return result.fetchall()

def get_device(id):
  sql = "SELECT equipment.id, equipment.model, manufacturers.name, invcount.count, users.username creator FROM equipment, manufacturers, users, userequipment, (SELECT COUNT(*) FROM inventory WHERE model_id=:id) AS invcount WHERE equipment.id=:id AND manufacturers.id=equipment.manufacturer_id AND userequipment.equipment_id=:id AND users.id=userequipment.user_id"
  result = db.session.execute(sql, {"id" : id})
  return result.fetchone()

def insert_device(model, manufacturer_id):
  if user_id() == 0:
    raise UserAuthorityError("User not logged in")

  sql = "INSERT INTO equipment (model, manufacturer_id, visible) VALUES (:model, :manufacturer_id, TRUE) RETURNING id"
  result = db.session.execute(sql, {"model" : model, "manufacturer_id" : manufacturer_id})
  equipment_id = result.fetchone()[0]
  sql = "INSERT INTO userequipment (user_id, equipment_id) VALUES (:user_id, :equipment_id)"
  db.session.execute(sql, { "user_id": user_id(), "equipment_id": equipment_id })
  db.session.commit()

def get_user_id_from_device(equipment_id):
  sql = "SELECT user_id FROM userequipment WHERE equipment_id=:equipment_id"
  result = db.session.execute(sql, { "equipment_id": equipment_id })
  return result.fetchone()[0]

def remove_device(equipment_id):
  if user_id() != get_user_id_from_device(equipment_id):
    raise UserAuthorityError("No authority to delete this device")

  sql = "DELETE FROM equipment WHERE id=:equipment_id"
  db.session.execute(sql, { "equipment_id": equipment_id })
  db.session.commit()