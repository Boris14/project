import hashlib

from database import DB

from itsdangerous import (
        TimedJSONWebSignatureSerializer as Serializer,
        BadSignature,
        SignatureExpired
        )

SECRET_KEY = 'ncXZyx5cLR7x1$B^Ybtqp1f!E#dG4H3EN@ioYYKoxx'

class User:
    def __init__(self, id, username, password, email, phone, adress):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.adress = adress


    def create(self):
        with DB() as db:
            values = (self.username, self.password, self.email, self.phone, self.adress)
            db.execute('''
                INSERT INTO users (username, password, email, phone, adress)
                VALUES (?, ?, ?, ?, ?)''', values)
            return self


    @staticmethod
    def find_by_username(username):
        if not username:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            if row:
                return User(*row)

    @staticmethod
    def find_by_id(id):
        if not id:
            return None
        with DB() as db:
            row = db.execute(
                'SELECT * FROM users WHERE id = ?',
                (id,)
            ).fetchone()
            if row:
                return User(*row)

    def delete(self):
        with DB() as db:
            db.execute('DELETE FROM users WHERE id = ?', (self.id,))


    @staticmethod
    def hash_password(password):
        return hashlib.sha256(password.encode('utf-8')).hexdigest()


    def verify_password(self, password):
        return self.password == hashlib.sha256(password.encode('utf-8')).hexdigest()

    def generate_token(self):
        s = Serializer(SECRET_KEY, expires_in=600)
        return s.dumps({'username': self.username})

    @staticmethod
    def verify_token(token):
        s = Serializer(SECRET_KEY)
        try:
            s.loads(token)
        except SignatureExpired:
            return False
        except BadSignature:
            return False
        return True



