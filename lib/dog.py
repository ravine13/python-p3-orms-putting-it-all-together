import sqlite3

CONN = sqlite3.connect('lib/dogs.db')
CURSOR = CONN.cursor()

class Dog:

    dog_count = 0

    def __init__(self, name, breed):
        self.name = name
        self.breed = breed
        self.id = Dog.dog_count  
        Dog.dog_count += 1  

    def get_name(self):
        return self.name
    
    def get_breed(self):
        return self.breed
    
    def get_id(self):
        return self.id
    
    def set_name(self,new_name):
        self.name = new_name

    def set_breed(self,new_breed):
        self.breed = new_breed

    @classmethod
    def create_table(cls):
         
        sql="""CREATE TABLE IF NOT EXISTS dogs(
           id INTEGER PRIMARY KEY,
           name TEXT,
           breed TEXT            
                       
        )"""
        CURSOR.execute(sql)
        CONN.commit()
       
    @classmethod
    def drop_table(self):
        sql="DROP TABLE IF EXISTS dogs"
        CURSOR.execute(sql)
        CONN.commit()
    
    def save(self):
        sql = """
        INSERT INTO dogs (name, breed)
        VALUES (?, ?)
    """
        values = (self.name, self.breed)
        CURSOR.execute(sql, values)
        self.id = CURSOR.lastrowid
        CONN.commit()

    @classmethod
    def create(cls,name,breed):
        new_dog = cls(name,breed)
        new_dog.save()

        return new_dog
    @classmethod
    def new_from_db(cls,row):
        new_dog = cls(row[1],row[2])
        new_dog.id = row[0]

        return new_dog
    
    @classmethod
    def get_all(cls):
        sql = "SELECT *FROM dogs"
        CURSOR.execute(sql)
        rows=CURSOR.fetchall()
        cls.dogs = [cls.new_from_db(row)for row in rows]

        return cls.dogs
    
    @classmethod
    def find_by_name_and_breed(cls,name):
        sql="SELECT * FROM dogs WHERE name=? LIMIT 1"
        dog=CURSOR.execute(sql,(name,)).fetchone()
        if dog:
            return cls.new_from_db(dog)
        else:
            return None
        
    
    @classmethod
    def find_by_id(cls,id):
        sql="SELECT * FROM dogs WHERE id=?"
        dog=CURSOR.execute(sql,(id,)).fetchone()
        return cls.new_from_db(dog)

    @classmethod
    def 