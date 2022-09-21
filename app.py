from flask import Flask, render_template, jsonify, request
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
        return '<User>' + self.username

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

#Read
@app.route('/showstudents', methods=['GET'])
def get_student():
    students = db.session.query(Batch).all()
    return render_template('home.html',students=students)

#Update
@app.route('/updaterecord', methods=['PUT'])
def update_student():
    try:
        stud = db.session.query(Batch).filter(Batch.id==request.json["id"]).first()
        stud.username = request.json['username']
        stud.email = request.json['email']
        stud.grade = request.json['grade']
        db.session.commit()
        return 'Student record updated!'
    except Exception as e:
        print(e)
        return 'Student record updation Failed!'

#Delete
@app.route('/deleterecord',methods=['DELETE'])
def delete_student():
    try:
        stud = db.session.query(Batch).filter(Batch.id == request.json['id']).first()
        db.session.delete(stud)
        db.session.commit()
        return 'Student ' + stud.username + ' is deleted!', 200
    except Exception as e:
        print(e)
        return 'Student record deletion Failed!', 422

if __name__ == '__main__':
    app.run(debug=True)
