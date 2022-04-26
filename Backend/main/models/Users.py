from .. import db
# from flask import jsonify

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    poems = db.relationship('Poem', back_populates="user", cascade="all, delete-orphan")
    ratings = db.relationship('Rating', back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return '<User: %r %r %r %r >' % (self.username, self.password, self.role, self.email)

    # Convertir objeto en JSON
    def to_json(self):
        user_json = { 
            'id': self.id,
            'username': str(self.username),
            # 'password': str(self.password),
            # 'role': str(self.role),
            # 'email': str(self.email),
            'poems': [poem.to_json_short() for poem in self.poems],
            'poem_amount': len(self.poems),
            'rating_amount': len(self.ratings),
        }
        return user_json

    def to_json_short(self):
        user_json = {
            'id': self.id,
            'username': str(self.username),
        }
        return user_json
    @staticmethod

    # Convertir JSON a objeto
    def from_json(user_json):
        username = user_json.get('username')
        password = user_json.get('password')
        role = user_json.get('role')
        email = user_json.get('email')
        return User(username=username, 
                    password=password, 
                    role=role, 
                    email=email,
                    )
