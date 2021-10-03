from app import app
from flask import render_template, request, redirect
from services.equipment import get_equipment, get_device, insert_device, remove_device
from services.inventory import get_inventory_for_device, insert_entry_for_device
from services.manufacturers import get_all_manufacturers, insert_manufacturer
from services.productions import insert_production, get_all_productions, get_production

@app.route("/")
def index():
  list = get_equipment()
  return render_template("index.html", equipment=list)

@app.route("/equipment/<int:id>")
def device(id):
  deviceInventory = get_inventory_for_device(id)
  device = get_device(id)
  return render_template("device.html", inventory=deviceInventory, device=device)

@app.route("/create")
def create():
  return redirect("/create/device")
  
@app.route("/create/device", methods=["GET", "POST"])
def create_device():
  if request.method == "POST":
    insert_device(request.form["model"], request.form["manufacturer_id"])
    return redirect("/")

  list = get_all_manufacturers()
  return render_template("create-device.html", manufacturers=list)

@app.route("/create/manufacturer", methods=["GET", "POST"])
def create_manufacturer():
  if request.method == "POST":
    insert_manufacturer(request.form["name"])
    return redirect("/create")

  return render_template("create-manufacturer.html")

@app.route("/create/inventory/<int:id>", methods=["GET", "POST"])
def create_device_entry(id):
  if request.method == "POST":
    serialnum = request.form["serialnum"]

    if len(serialnum) < 2:
      return render_template("error.html", errormessage="The provided serial number was too short.")

    insert_entry_for_device(id, serialnum, True)
    redirUrl = "/equipment/" + str(id)
    return redirect(redirUrl)

  device = get_device(id)
  return render_template("create-entry.html", device=device)

@app.route("/create/production", methods=["GET", "POST"])
def create_production():
  if request.method == "POST":
    name = request.form["name"]
    starting = request.form["starting"]
    ending = request.form["ending"]

    if len(name) < 1:
      return render_template("error.html", errormessage="No production name was provided")

    insert_production(name, starting, ending)
    return redirect("/productions")
    
  return render_template("create-production.html")

@app.route("/remove/<int:id>")
def remove_device(id):
  remove_device(id)
  return redirect("/")

@app.route("/productions")
def productions_page():
  list = get_all_productions()
  return render_template("productions.html", productions=list)

@app.route("/productions/<int:production_id>")
def production(production_id):
  production = get_production(production_id)
  return render_template("production.html", production=production)