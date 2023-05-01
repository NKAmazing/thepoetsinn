from .. import db
from . import UserModel, PoemModel

# Modelo de Rating
class Rating(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    commentary = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poem_id = db.Column(db.Integer, db.ForeignKey('poem.id'), nullable=False)

    user = db.relationship('User', back_populates="ratings", uselist=False, single_parent=True)
    poem = db.relationship('Poem', back_populates="ratings", uselist=False, single_parent=True)

    def __repr__(self):
        return '<Rating: %r %r %r %r >' % (self.score, self.commentary, self.user_id, self.poem_id)

    # Convertir objeto en JSON
    def to_json(self):
        rating_json = { 
            'id': self.id,
            'score': self.score,
            'commentary': str(self.commentary),
            'user': self.user.to_json_short(),
            'poem': self.poem.to_json_short(),
        }
        return rating_json

    def to_json_short(self):
        rating_json = {
            'id': self.id,
            'score': self.score,
            'commentary': str(self.commentary),
            # 'user': self.user.to_json(),
            # 'poem': self.poem.to_json(),
        }
        return rating_json
    @staticmethod

    # Convertir JSON a objeto
    def from_json(rating_json):
        id = rating_json.get('id')
        score = rating_json.get('score')
        commentary = rating_json.get('commentary')
        user_id = rating_json.get('user_id')
        poem_id = rating_json.get('poem_id')
        return Rating(id=id,
                    score=score,
                    commentary=commentary,
                    user_id=user_id,
                    poem_id=poem_id,
                    )
