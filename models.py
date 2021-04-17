from extensions import db
import uuid

log_food = db.Table('log_food',
                    db.Column('date_id', db.Integer, db.ForeignKey('date.id'), primary_key=True),
                    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
                    )


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, unique=True, nullable=False)
    proteins = db.Column(db.Integer, nullable=False)
    carbs = db.Column(db.Integer, nullable=False)
    fats = db.Column(db.Integer, nullable=False)
    deleted = db.Column(db.Boolean, default=False)
    quantity = db.Column(db.Integer, default=1)
    serving_unit = db.Column(db.String, nullable=False)

    @property
    def calories(self):
        return self.proteins * 4 + self.carbs * 4 + self.fats * 9

    @staticmethod
    def get_arguments():
        not_required = ['id', 'public_id', 'deleted']
        return [column.name for column in Food.__table__.columns if column.name not in not_required]

    __mapper_args__ = {
        "order_by": id.desc()
    }


class Date(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=False)
    foods = db.relationship('Food', secondary=log_food, lazy='dynamic')

    __mapper_args__ = {
        "order_by": id.desc()
    }
