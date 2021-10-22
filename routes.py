from app import app
from exceptions import UserAuthorityError
from flask import render_template, request, redirect, session
from services.equipment import get_equipment, get_device, insert_device, remove_device, update_device
from services.inventory import check_availability, get_inventory_for_device, insert_entry_for_device, get_user_inventory_count
from services.manufacturers import get_all_manufacturers, insert_manufacturer
from services.productions import insert_production, get_all_productions, get_production
from services.users import check_user_credentials, create_user, get_username, user_id, end_session
from services.reservations import create_reservation, delete_reservation, get_reservations_for_production, start_reservation_mode, stop_reservation_mode, reservation_mode_production_id, is_device_reserved, delete_reservation


@app.route("/")
def index():
  return redirect("/equipment")

@app.route("/login", methods=["GET", "POST"])
def login():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]

    if not check_user_credentials(username, password):
      notification = { 
        "message": "Wrong password or username. Please try again.",
        "type": "error"
       }
      return render_template("login.html", notification=notification)

    return redirect("/")

  if user_id() != 0:
    return redirect("/user")
  return render_template("login.html")

@app.route("/user")
def user_page():
  if user_id() == 0:
    return redirect("/login")
  
  inventory_count = get_user_inventory_count(user_id())
  return render_template("user.html", inventory_count = inventory_count)

@app.route("/logout")
def logout():
  end_session()
  return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
  if request.method == "POST":
    username = request.form["username"]
    password = request.form["password"]
    is_admin = request.form.get("admin") != None
    
    if len(username) < 4 | len(password) < 6:
      return render_template("error.html", errormessage="Username min 4 characters, password min 6 characters")

    if create_user(username, password, is_admin):
      return redirect("/")

    return render_template("error.html", errormessage="Registration failed")

  return render_template("register.html")

@app.route("/equipment/<int:id>")
def device(id):
  deviceInventory = get_inventory_for_device(id)
  device = get_device(id)

  if reservation_mode_production_id() != 0:
    production = get_production(reservation_mode_production_id())
    availability = []
    for entry in deviceInventory:
      availability.append(check_availability(entry.id, production))
    notification = { "type": "reserving" }
    return render_template("equipment.html", inventory=deviceInventory, device=device, availability=availability, notification=notification)

  return render_template("equipment.html", inventory=deviceInventory, device=device)

@app.route("/equipment")
def equipment_list():
  list = get_equipment()

  if reservation_mode_production_id() != 0:
    notification = { "type": "reserving" } 
    return render_template("equipment_list.html", equipment=list, notification=notification)

  return render_template("equipment_list.html", equipment=list)

@app.route("/create")
def create():
  return redirect("/create/device")
  
@app.route("/create/device", methods=["GET", "POST"])
def create_device():
  if request.method == "POST":
    device_model = request.form["model"]
    manufacturer_id = request.form["manufacturer_id"]

    if len(device_model) < 3:
      return render_template("error.html", errormessage="Name of model is too short")
    try:
      insert_device(device_model, manufacturer_id)
      return redirect("/")
    except UserAuthorityError as error:
      return render_template("error.html", errormessage=error.message) 

  manufacturers = get_all_manufacturers()
  manuufacturer_dicts = []
  for manufacturer in manufacturers:
    dictionary = {"value": manufacturer.id, "label": manufacturer.name}
    manuufacturer_dicts.append(dictionary)

  if user_id() == 0:
    notification = {
      "type": "info",
      "message": "Log in to edit the inventory"
    }
    return render_template("create-device.html", notification=notification, manufacturers=manuufacturer_dicts)

  return render_template("create-device.html", manufacturers=manuufacturer_dicts)

@app.route("/create/manufacturer", methods=["GET", "POST"])
def create_manufacturer():
  if request.method == "POST":
    manufacturer_name = request.form["name"]
    if len(manufacturer_name) < 1:
      return render_template("error.html", errormessage="Name of manufacturer is too short")

    try:
      insert_manufacturer(manufacturer_name)
      return redirect("/create")
    except UserAuthorityError as error:
      return render_template("error.html", errormessage=error.message) 

  if user_id() == 0:
    notification = {
      "type": "info",
      "message": "Log in to edit the inventory"
    }
    return render_template("create-manufacturer.html", notification=notification)

  return render_template("create-manufacturer.html")

@app.route("/create/inventory/<int:id>", methods=["GET", "POST"])
def create_device_entry(id):
  if request.method == "POST":
    serialnum = request.form["serialnum"]

    if len(serialnum) < 2:
      return render_template("error.html", errormessage="The provided serial number was too short.")

    try:
      insert_entry_for_device(id, serialnum)
      return redirect("/equipment/" + str(id))
    except UserAuthorityError as error:
      return render_template("error.html", errormessage=error.message)

  device = get_device(id)

  if user_id() == 0:
    notification = {
      "type": "info",
      "message": "Log in to edit the inventory"
    }
    return render_template("create-entry.html", notification=notification, device=device)

  return render_template("create-entry.html", device=device)

@app.route("/create/production", methods=["GET", "POST"])
def create_production():
  if request.method == "POST":
    name = request.form["name"]
    starting = request.form["starting"]
    ending = request.form["ending"]

    if len(name) < 1:
      return render_template("error.html", errormessage="No production name was provided")
    try:
      insert_production(name, starting, ending)
      return redirect("/productions")
    except UserAuthorityError as error:
      return render_template("error.html", errormessage=error.message)

  if user_id() == 0:
    notification = {
      "type": "info",
      "message": "Log in to edit the inventory"
    }
    return render_template("create-production.html", notification=notification)
    
  return render_template("create-production.html")

@app.route("/reserve/<int:production_id>", methods=["POST"])
def reserve_device(production_id):

  for inventory_id, value in request.form.items():
    print(inventory_id)
    print(value)
    print(is_device_reserved(inventory_id, production_id))
    if value == "1" and not is_device_reserved(inventory_id, production_id):
      print("reserving")
      create_reservation(inventory_id, production_id)

    if value == "0" and is_device_reserved(inventory_id, production_id):
      print("deleting")
      delete_reservation(inventory_id, production_id)
      
  return redirect("/")

@app.route("/reserve")
def activate_reservation_mode():
  if reservation_mode_production_id() != 0:
    stop_reservation_mode()
    return redirect("/equipment")

  production_id = request.args.get("production")

  if not production_id:
    return render_template("error.html", errormessage="No production id provided")

  try:
    start_reservation_mode(production_id)
  except UserAuthorityError as error:
    return render_template("error.html", errormessage=error.message)

  return redirect("/equipment") 

@app.route("/remove/<int:id>")
def remove_device_from_equipment(id):
  try:
    remove_device(id)
    return redirect("/")
  except UserAuthorityError as error:
    return render_template("error.html", errormessage=error.message)

@app.route("/edit/device/<int:device_id>", methods = ["POST", "GET"])
def edit_device(device_id):
  if request.method == "POST":
    model_to_set = request.form["model"]
    manufacturer_id_to_set = request.form["manufacturer_id"]

    if len(model_to_set) < 3:
      return render_template("error.html", errormessage="Name of model is too short")
    try:
      update_device(device_id, model_to_set, manufacturer_id_to_set)
      return redirect("/equipment/%s" % device_id)
    except UserAuthorityError as error:
      return render_template("error.html", errormessage=error.message) 

  device = get_device(device_id)
  manufacturers = get_all_manufacturers()
  manuufacturer_dicts = []
  for manufacturer in manufacturers:
    dictionary = {"value": manufacturer.id, "label": manufacturer.name}
    manuufacturer_dicts.append(dictionary)
  return render_template("edit-device.html", device = device, manufacturers = manuufacturer_dicts)

@app.route("/productions")
def productions_page():
  list = get_all_productions()
  return render_template("production_list.html", productions=list)

@app.route("/productions/<int:production_id>")
def production(production_id):
  production = get_production(production_id)
  reservations = get_reservations_for_production(production_id)
  return render_template("production.html", production=production, reservations=reservations)