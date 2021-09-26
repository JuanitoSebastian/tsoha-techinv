from app import app
from flask import render_template, request, redirect
import equipment
import inventory
import manufacturers

@app.route("/")
def index():
  list = equipment.get_list()
  return render_template("index.html", equipment=list)

@app.route("/equipment/<int:id>")
def device(id):
  deviceInventory = inventory.get_device_inventory(id)
  device = equipment.get_device(id)
  return render_template("device.html", inventory=deviceInventory, device=device)

@app.route("/insert-device", methods=["POST"])
def insert_device():
  equipment.insert_device(request.form["model"], request.form["manufacturer_id"])
  return redirect("/")

@app.route("/insert-entry/<int:id>", methods=["POST"])
def insert_inventory_entry(id):
  inventory.insert_entry(id, request.form["serialnum"], True)
  redirUrl = "/equipment/" + str(id)
  return redirect(redirUrl)

@app.route("/insert-manufacturer", methods=["POST"])
def insert_manufacturer():
  manufacturers.insert_manufacturer(request.form["name"])
  return redirect("/create")

@app.route("/create")
def create():
  return redirect("/create/device")
  
@app.route("/create/device")
def create_device():
  list = manufacturers.get_list()
  return render_template("create-device.html", manufacturers=list)

@app.route("/create/manufacturer")
def create_manufacturer():
  return render_template("create-manufacturer.html")

@app.route("/create/inventory/<int:id>")
def create_device_entry(id):
  device = equipment.get_device(id)
  return render_template("create-entry.html", device=device)

@app.route("/remove/<int:id>")
def remove_device(id):
  equipment.remove_device(id)
  return redirect("/")