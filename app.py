from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema
from webargs import fields, validate
from webargs.flaskparser import use_args
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False, unique=True)
    grade = db.Column(db.String(1), nullable=False)

    def __repr__(self) -> str:
        return '<User %r>' % self.username

class BatchSchema(Schema):
    username = fields.String(required=True, validate=validate.Length(min=5,max=50))
    email = fields.Email(required=True)
    grade = fields.String(required=True, validate=validate.Length(max=1))

#Insertion
@app.route('/student', methods=['POST'])
@use_args(BatchSchema,location='json')
def add_student(kwargs):
    try:
        student = Batch(**kwargs)
        db.session.add(student)
        db.session.commit()
        return "Student added!"
    except Exception as e:
        print(e)
        return "Student addtion Failed!"

if __name__ == '__main__':
    app.run(debug=True)
