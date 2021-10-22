from db import db
import secrets
from werkzeug.security import check_password_hash, generate_password_hash
from flask import session

def check_if_user_exists(username):
  sql = "SELECT COUNT(*) FROM users WHERE username=:username"
  result = db.session.execute(sql, { "username":username }).fetchone()

  if result.count > 0:
    return True

  return False

def check_user_credentials(username, password):
  sql = "SELECT id, username, password FROM users WHERE username=:username"
  result = db.session.execute(sql, { "username":username })
  user = result.fetchone()

  if not user:
    # Invalid username
    return False
  else:
    if check_password_hash(user.password, password):
      # Correct password 
      initiate_session(user.id, user.username)
      return True
    else:
      # Incorrect password
      return False

def initiate_session(user_id_to_set, username_to_set):
  session["user_id"] = user_id_to_set
  session["username"] = username_to_set
  session["csrf_token"] = secrets.token_hex(16)


def create_user(username, password, is_admin):
  hash_value = generate_password_hash(password)

  try:
    sql = "INSERT INTO users (username, password, isAdmin) VALUES (:username, :password, :isAdmin)"
    db.session.execute(sql, { "username":username, "password":hash_value , "isAdmin":is_admin })
    db.session.commit()
  except:
    return False
  
  return True

def get_username(user_id):
  if user_id == 0: return None

  sql = "SELECT username FROM users WHERE id=:id"
  result = db.session.execute(sql, { "id":user_id })
  user = result.fetchone()

  return user.username  

def user_id():
  return session.get("user_id", 0)

def get_csrf_token():
  return session.get("csrf_token")

def is_user_admin():
  if user_id() == 0: return False
  sql = "SELECT isAdmin FROM users WHERE id=:user_id"
  result = db.session.execute(sql, { "user_id": user_id() })
  is_admin = result.fetchone()[0]
  return is_admin

def end_session():
  del session["user_id"]
  del session["username"]
  del session["csrf_token"]