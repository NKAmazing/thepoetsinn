from .. import db

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    commentary = db.Column(db.String(100), nullable=True)
    user_id = db.Column(db.Integer)
    poem_id = db.Column(db.Integer)


    def __repr__(self):
        return '<Rating: %r %r %r %r >' % (self.score, self.commentary, self.user_id, self.poem_id)

    # Convertir objeto en JSON
    def to_json(self):
        rating_json = { 
            'id': self.id,
            'score': self.score,
            'commentary': str(self.commentary),
            'user_id': (self.user_id),
            'poem_id': (self.poem_id),
        }
        return rating_json

    def to_json_short(self):
        rating_json = {
            'id': self.id,
            'score': self.score,
            'commentary': str(self.commentary),
        }
        return rating_json
    @staticmethod

    # COnvertir JSON a objeto
    def from_json(rating_json):
        id = rating_json.get('id')
        score = rating_json.get('score')
        commentary = rating_json.get('commentary')
        user_id = rating_json.get('user_id')
        poem_id = rating_json.get('poem id')
        return Rating(id=id,
                    score=score,
                    commentary=commentary,
                    user_id=user_id,
                    poem_id=poem_id,
                    )
