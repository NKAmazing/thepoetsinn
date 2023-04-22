from .. import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    poems = db.relationship('Poem', back_populates="user", cascade="all, delete-orphan")
    ratings = db.relationship('Rating', back_populates="user", cascade="all, delete-orphan")

    @property
    def plain_password(self):
        raise AttributeError("Not allowed")
    
    @plain_password.setter
    def plain_password(self, password):
        self.password = generate_password_hash(password)

    def generate_password(self, password):
        return generate_password_hash(password)

    def validate_pass(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User: %r %r %r %r >' % (self.username, self.password, self.role, self.email)

    # Convertir objeto en JSON
    def to_json(self):
        user_json = { 
            'id': self.id,
            'username': str(self.username),
            'email': str(self.email),
            'role': str(self.role),
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

    def to_json_admin(self):
        user_json = { 
            'id': self.id,
            'username': str(self.username),
            'email': str(self.email),
            'password': str(self.password),
            'role': str(self.role),
            'poems': [poem.to_json_short() for poem in self.poems],
            'poem_amount': len(self.poems),
            'rating_amount': len(self.ratings),
        }
        return user_json

    def to_json_public(self):
        user_json = {
            'id': self.id,
            'username': str(self.username),
            'poems': [poem.to_json_short() for poem in self.poems],
            'poem_amount': len(self.poems),
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
                    role=role, 
                    email=email,
                    plain_password=password,
                    )
