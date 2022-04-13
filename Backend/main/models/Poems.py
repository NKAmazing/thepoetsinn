from .. import db
import datetime


class Poem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    body = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime, nullable=False, default=datetime.datetime.now())
    

    def __repr__(self):
        return '<Poem: %r %r %r %r >' % (self.title, self.body, self.user_id, self.date_time)

    # Convertir objeto en JSON
    def to_json(self):
        poem_json = { 
            'id': self.id,
            'title': str(self.title),
            'body': str(self.body),
            'user_id': int(self.user_id),
            'date_time': str(self.date_time),
        }
        return poem_json

    def to_json_short(self):
        poem_json = {
            'id': self.id,
            'title': str(self.title),
            'body': str(self.body),
        }
        return poem_json
    @staticmethod

    # Convertir JSON a objeto
    def from_json(poem_json):
        id = poem_json.get('id')
        title = poem_json.get('title')
        body = poem_json.get('body')
        user_id = poem_json.get('user_id')
        date_time = poem_json.get('date_time')
        return Poem(id=id,
                    title=title, 
                    body=body, 
                    user_id=user_id, 
                    date_time=date_time,
                    )

