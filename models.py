from extensions import db
import uuid

log_food = db.Table('log_food',
                    db.Column('date_id', db.Integer, db.ForeignKey('date.id'), primary_key=True),
                    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
                    )


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, default=str(uuid.uuid4()))
    name = db.Column(db.String(50), unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False)

    @property
    def calories(self):
        return self.proteins * 4 + self.carbs * 4 + self.fats * 9

    @staticmethod
    def get_arguments():
        not_required = ['id', 'public_id', 'deleted']
        return [column.name for column in Food.__table__.columns if column.name not in not_required]


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, default=str(uuid.uuid4()))
    date = db.Column(db.String, nullable=False)
    foods = db.relationship('Food', secondary=log_food, lazy='dynamic')
