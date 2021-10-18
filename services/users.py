from db import db
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
    print("Invalid username!")
    return False
  else:
    if check_password_hash(user.password, password):
      # Correct password 
      print("Correct password")
      session["user_id"] = user.id
      session["username"] = user.username
      return True
    else:
      # Incorrect password
      print("Incorrect password")
      return False


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

def end_session():
  del session["user_id"]
  del session["username"]