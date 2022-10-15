from database.createdb import cursor
from database.createdb import db

def tofile(names):
    new = []
    for name in names:
        new.append(name[0])
    return new

def create_db():
    cursor.execute("CREATE TABLE IF NOT EXISTS settings (category INT, adminrole INT, channel_num INT, qiwi TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS shop (name TEXT, price INT)")
    db.commit()

def createtables():
    cursor.execute("SELECT category FROM settings")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO settings VALUES (?,?,?,?)", (-1, -1, 0, "Не установлена"))
        db.commit()

def editadmin(id):
    cursor.execute(f"UPDATE settings SET adminrole = {id}")
    db.commit()

def editcategory(id):
    cursor.execute(f"UPDATE settings SET category = {id}")
    db.commit()

def getadmin():
    cursor.execute("SELECT adminrole FROM settings")
    return cursor.fetchone()[0]

def getcategory():
    cursor.execute("SELECT category FROM settings")
    return cursor.fetchone()[0]

def getnumber():
    cursor.execute("SELECT channel_num FROM settings")
    return cursor.fetchone()[0]

def addnumber():
    cursor.execute("SELECT channel_num FROM settings")
    value = cursor.fetchone()[0] + 1
    cursor.execute(f"UPDATE settings SET channel_num = {value}")
    db.commit()

def addproduct(name: str, price: int):
    cursor.execute(f"SELECT name FROM shop WHERE name = '{name}'")
    answer = cursor.fetchone()
    if answer is not None:
        return False
    else:
        cursor.execute("INSERT INTO shop VALUES (?,?)", (name, price))
        db.commit()
        with open("catalog.txt", "w") as file:
            cursor.execute("SELECT name FROM shop")
            text = ""
            for i in tofile(cursor.fetchall()):
                text += i + "&&"
            file.write(text.strip())
        return True

def removeproduct(name: str):
    cursor.execute(f"SELECT name FROM shop WHERE name = '{name}'")
    answer = cursor.fetchone()
    if answer is not None:
        cursor.execute(f"DELETE FROM shop WHERE name = '{name}'")
        db.commit()
        with open("catalog.txt", "w") as file:
            cursor.execute("SELECT name FROM shop")
            text = ""
            for i in tofile(cursor.fetchall()):
                text += i + "&&"
            file.write(text.strip())
        return True
    else:
        return False

def shopcatalog():
    cursor.execute(f"SELECT * FROM shop")
    return cursor.fetchall()

def updatenames():
    with open("catalog.txt", "w") as file:
        cursor.execute("SELECT name FROM shop")
        text = ""
        for i in tofile(cursor.fetchall()):
            text += i + "&&"
        file.write(text.strip())

def getprice(name):
    cursor.execute(f"SELECT price FROM shop WHERE name = '{name}'")
    return cursor.fetchone()[0]

def editqiwi(value: str):
    cursor.execute(f"UPDATE settings SET qiwi = '{value}'")
    db.commit()

def getqiwi():
    cursor.execute(f"SELECT qiwi FROM settings")
    return cursor.fetchone()[0]