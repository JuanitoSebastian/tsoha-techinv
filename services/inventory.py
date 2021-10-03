from db import db

def get_inventory_for_device(id):
  sql = "SELECT id, serialnum, available FROM inventory WHERE model_id=:id"
  result = db.session.execute(sql, {"id" : id})
  return result.fetchall()

def insert_entry_for_device(model_id, serialnum, available):
  sql = "INSERT INTO inventory (model_id, serialnum, available) VALUES (:model_id, :serialnum, :available)"
  db.session.execute(sql, {"model_id" : model_id, "serialnum" : serialnum, "available" : available})
  db.session.commit()