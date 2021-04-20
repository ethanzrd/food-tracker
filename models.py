from flask_login import UserMixin

from extensions import db
from sqlalchemy.orm import relationship

log_food = db.Table('log_food',
                    db.Column('date_id', db.Integer, db.ForeignKey('date.id'), primary_key=True),
                    db.Column('food_id', db.Integer, db.ForeignKey('food.id'), primary_key=True)
                    )


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    confirmed_email = db.Column(db.Boolean, default=False)
    join_date = db.Column(db.String)
    dates = relationship('Date', back_populates='user')
    foods = relationship('Food', back_populates='user')


class Food(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='foods')
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = relationship('User', back_populates='dates')
    date = db.Column(db.String, nullable=False)
    foods = db.relationship('Food', secondary=log_food, lazy='dynamic')

    __mapper_args__ = {
        "order_by": id.desc()
    }
