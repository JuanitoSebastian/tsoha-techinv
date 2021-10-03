from db import db

def get_equipment():
  sql = "SELECT equipment.id, equipment.model, manufacturers.name manufacturer, COALESCE(invcount.count, 0) count FROM (SELECT * FROM equipment WHERE visible=TRUE) AS equipment JOIN manufacturers ON manufacturers.id=equipment.manufacturer_id LEFT JOIN (SELECT model_id, COUNT(model_id) FROM inventory GROUP BY model_id) AS invcount ON invcount.model_id=equipment.id"
  result = db.session.execute(sql)
  return result.fetchall()

def get_device(id):
  sql = "SELECT equipment.id, equipment.model, manufacturers.name, invcount.count FROM equipment, manufacturers, (SELECT COUNT(*) FROM inventory WHERE model_id=:id) AS invcount WHERE equipment.id=:id AND manufacturers.id=equipment.manufacturer_id"
  result = db.session.execute(sql, {"id" : id})
  return result.fetchone()

def insert_device(model, manufacturer_id):
  sql = "INSERT INTO equipment (model, manufacturer_id, visible) VALUES (:model, :manufacturer_id, TRUE)"
  db.session.execute(sql, {"model" : model, "manufacturer_id" : manufacturer_id})
  db.session.commit()

def remove_device(id):
  sql = "UPDATE equipment SET visible=FALSE WHERE id=:id"
  db.session.execute(sql, { "id":id })
  db.session.commit()