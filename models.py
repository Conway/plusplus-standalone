from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Thing(db.Model):
    __tablename__ = 'Item'
    item = db.Column(db.String, primary_key=True, unique=True)
    points = db.Column(db.Integer, default=0)
    user = db.Column(db.Boolean)

    def increment(self):
        self.points += 1

    def decrement(self):
        self.points -= 1
