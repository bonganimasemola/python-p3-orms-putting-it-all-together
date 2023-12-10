import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed, id=None):
        self.id = id
        self.name = name
        self.breed = breed

    @staticmethod
    def create_table():
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @staticmethod
    def drop_table():
       sql = """
       DROP TABLE IF EXISTS dogs
       """
       CURSOR.execute(sql)
       print("Executed SQL:", sql)
       CONN.commit()


    def save(self):
        sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
        CURSOR.execute(sql, (self.name, self.breed))
        CONN.commit()
        
    @staticmethod
    def create(name, breed):
       dog = Dog(name, breed)
       dog.save()
       return dog

    @staticmethod
    def new_from_db(row):
       return Dog(row[1], row[2], row[0])

    @staticmethod
    def get_all():
       rows = CURSOR.execute("SELECT * FROM dogs").fetchall()
       dogs = [Dog.new_from_db(row) for row in rows]
       return dogs

    @staticmethod
    def find_by_name(name):
       rows = CURSOR.execute("SELECT * FROM dogs WHERE name = ?", (name,)).fetchall()
       if rows:
           return Dog.new_from_db(rows[0])
       else:
           return None

    @staticmethod
    def find_by_id(id):
       rows = CURSOR.execute("SELECT * FROM dogs WHERE id = ?", (id,)).fetchall()
       if rows:
           return Dog.new_from_db(rows[0])
       else:
           return None

    @staticmethod
    def find_or_create_by(name, breed):
       dog = Dog.find_by_name(name)
       if dog is None:
           dog = Dog.create(name, breed)
       return dog

    def update(self):
       sql = """
           UPDATE dogs
           SET name = ?, breed = ?
           WHERE id = ?
       """
       CURSOR.execute(sql, (self.name, self.breed, self.id))
       CONN.commit()
