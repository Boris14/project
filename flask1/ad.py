from database import DB


class Ad:
    def __init__(self, id, title, description, price, date, is_active, buyer):
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.date = date
        self.is_active = is_active
        self.buyer = buyer
	

    @staticmethod
    def all():
        with DB() as db:
            rows = db.execute('SELECT * FROM ads').fetchall()
            return [Ad(*row) for row in rows]

    @staticmethod
    def find(id):
        with DB() as db:
            row = db.execute('SELECT * FROM ads WHERE id = ?', (id,)) \
                .fetchone()
            if not row:
                return Ad(0, "No ad","",0,"",False,"")
            return Ad(*row)


    def buy(self):
        with DB as db:
            db.execute('''UPDATE ads SET is_active = ?''', False);
        return self

    def create(self):
        with DB() as db:
            values = (self.title, self.description, self.price, self.date, self.is_active, self.buyer,)
            db.execute('''
                INSERT INTO ads (title, description, price, date, is_active, buyer)
                VALUES (?, ?, ?, ?, ?, ?)''', values)
            return self

    #def save(self):
      #  with DB() as db:
      #      values = (
        #        self.title, 
	#			self.description, 
	#			self.price, 
	#			self.date, 
	#			self.is_active, 
	#			self.buyer,
     #           self.id
     #       )
     #       db.execute(
     #           '''UPDATE ads
     #           SET title = ?, description = ?, price = ?, date = ?, is_active = ?, buyer = ?
     #           WHERE id = ?''', values)
     #       return self

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM ads WHERE id = ?', (self.id,))
