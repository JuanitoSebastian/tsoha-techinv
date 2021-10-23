from db import db
from services.users import user_id
from services.productions import get_production_name
from exceptions import UserAuthorityError
from flask import session


def create_reservation(inventory_id, production_id):
    if user_id() == 0:
        raise UserAuthorityError("User not logged in")

    # TODO: First check there are no other reservations
    sql = "INSERT INTO reservations (inventory_id, production_id) VALUES (:inventory_id, :production_id) RETURNING id"
    result = db.session.execute(sql, {"inventory_id": inventory_id, "production_id": production_id})
    reservation_id = result.fetchone()[0]
    sql = "INSERT INTO userreservations (user_id, reservation_id) VALUES (:user_id, :reservation_id)"
    db.session.execute(sql, {"user_id": user_id(), "reservation_id": reservation_id})
    db.session.commit()


def delete_reservation(inventory_id, production_id):
    if user_id() == 0:
        raise UserAuthorityError("User not logged in")

    sql = "DELETE FROM reservations WHERE inventory_id=:inventory_id AND production_id=:production_id"
    db.session.execute(
        sql, {"inventory_id": inventory_id, "production_id": production_id})
    db.session.commit()


def get_reservations_for_production(production_id):
    sql = "SELECT manufacturers.name manufacturer, equipment.model, inventory.serialnum \
        FROM manufacturers, equipment, inventory, reservations \
        WHERE reservations.production_id=:production_id AND reservations.inventory_id=inventory.id \
        AND equipment.id=inventory.model_id AND manufacturers.id=equipment.manufacturer_id"
    results = db.session.execute(sql, {"production_id": production_id})
    reservations = results.fetchall()
    return reservations


def is_device_reserved(inventory_id, production_id):
    sql = "SELECT COUNT(*) FROM reservations WHERE inventory_id=:inventory_id AND production_id=:production_id"
    result = db.session.execute(sql, {"inventory_id": inventory_id, "production_id": production_id})
    count = result.fetchone()[0]

    return count == 1


def start_reservation_mode(production_id):
    if user_id() == 0:
        raise UserAuthorityError("Log in to make reservations.")
        
    session["production_id"] = production_id
    session["production_name"] = get_production_name(production_id)


def stop_reservation_mode():
    del session["production_id"]
    del session["production_name"]


def reservation_mode_production_id():
    return session.get("production_id", 0)


def reservation_mode_production_name():
    return session.get("production_name")
