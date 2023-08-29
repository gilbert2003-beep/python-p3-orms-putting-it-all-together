import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = None

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS dogs (
                id INTEGER PRIMARY KEY,
                name TEXT,
                breed TEXT
            )
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        sql = "DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        if self.id is None:
            sql = "INSERT INTO dogs (name, breed) VALUES (?, ?)"
            values = (self.name, self.breed)
        else:
            sql = "UPDATE dogs SET name = ?, breed = ? WHERE id = ?"
            values = (self.name, self.breed, self.id)
        
        CURSOR.execute(sql, values)
        CONN.commit()
        
        if self.id is None:
            self.id = CURSOR.lastrowid

    @classmethod
    def new_from_db(cls, row):
        dog = cls(row[1], row[2])
        dog.id = row[0]
        return dog

    @classmethod
    def get_all(cls):
        sql = "SELECT * FROM dogs"
        CURSOR.execute(sql)
        rows = CURSOR.fetchall()
        return [cls.new_from_db(row) for row in rows]

    @classmethod
    def find_by_name(cls, name):
        sql = "SELECT * FROM dogs WHERE name = ?"
        CURSOR.execute(sql, (name,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_by_id(cls, id):
        sql = "SELECT * FROM dogs WHERE id = ?"
        CURSOR.execute(sql, (id,))
        row = CURSOR.fetchone()
        if row:
            return cls.new_from_db(row)
        return None

    @classmethod
    def find_or_create_by(cls, name, breed):
        dog = cls.find_by_name(name)
        if dog:
            return dog
        else:
            dog = cls(name, breed)
            dog.save()
            return dog

    def update(self):
        if self.id:
            self.save()

if __name__ == "__main__":
    Dog.create_table()
