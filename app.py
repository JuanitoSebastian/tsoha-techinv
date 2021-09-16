from flask import Flask
from flask import redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

@app.route("/")
def index():
  sql = "SELECT equipment.id, equipment.model, manufacturers.name manufacturer, COALESCE(invcount.count, 0) count FROM equipment JOIN manufacturers ON manufacturers.id=equipment.manufacturer_id LEFT JOIN (SELECT model_id, COUNT(model_id) FROM inventory GROUP BY model_id) AS invcount ON invcount.model_id=equipment.id"
  result = db.session.execute(sql)
  equipment = result.fetchall()
  return render_template("index.html", equipment=equipment)

@app.route("/equipment/<int:id>")
def device(id):
  sql = "SELECT serialnum, available FROM inventory WHERE model_id=:id"
  result = db.session.execute(sql, {"id" : id})
  inventory = result.fetchall()
  count = len(inventory)
  sql = "SELECT equipment.model, manufacturers.name, equipment.id FROM equipment, manufacturers WHERE equipment.id=:id AND manufacturers.id=equipment.manufacturer_id"
  result = db.session.execute(sql, {"id" : id})
  device = result.fetchone()
  return render_template("device.html", inventory=inventory, device=device, count=count)

@app.route("/insert-device", methods=["POST"])
def insertDevice():
  model = request.form["model"]
  manufacturer_id = request.form["manufacturer_id"]
  sql = "INSERT INTO equipment (model, manufacturer_id) VALUES (:model, :manufacturer_id)"
  db.session.execute(sql, {"model" : model, "manufacturer_id" : manufacturer_id})
  db.session.commit()
  return redirect("/")

@app.route("/insert-entry/<int:id>", methods=["POST"])
def insertInventoryEntry(id):
  serialnum = request.form["serialnum"]
  sql = "INSERT INTO inventory (model_id, serialnum, available) VALUES (:model_id, :serialnum, TRUE)"
  db.session.execute(sql, {"model_id" : id, "serialnum" : serialnum})
  db.session.commit()
  redirUrl = "/equipment/" + str(id)
  return redirect(redirUrl)
  
@app.route("/create")
def create():
  sql = "SELECT id, name FROM manufacturers"
  result = db.session.execute(sql)
  manufacturers = result.fetchall()
  return render_template("create.html", manufacturers=manufacturers)