from turtle import pd
from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db=SQLAlchemy(app)
class student(db.Model):
    __tablename__ = "student"
    id = db.Column(db.Integer, primary_key=True)
    s_id = db.Column(db.Integer(),unique = True)
    name = db.Column(db.String())
    age = db.Column(db.Integer())
    email= db.Column(db.String(80))
    def __init__(self, s_id,name,age,email):
        self.s_id = s_id
        self.name = name
        self.age = age
        self.email = email
    def __repr__(self):
        return f'student <{self.email}>'

@app.route('/create_student',methods=['POST'])
def create_student():
    data=request.get_json()
    try:
    # print(data['id'])
        u=student(
            s_id=data['s_id'],
            name=data['name'],
            age=data['age'],
            email=data['email']
        )
        db.session.add(u)
        db.session.commit()
        # return {"Msg":"ok","Data":data}
        return {
                    's_id' :u.s_id,'name':u.name,'age':u.age,'email':u.email
                },201
    except Exception as e:
        return  {"code": 404 ,"error": e.args}

@app.route('/get_all_student',methods=['GET'])
def get_all_student():
    Srudent_data=student.query.all()
    
    return jsonify([
            {
                's_id' :Srudent_data.s_id,'name':Srudent_data.name,'age':Srudent_data.age,'email':Srudent_data.email
            } for Srudent_data in student.query.all()
        ])

@app.route('/get_student_by_id/<int:id>/',methods=['GET'])
def get_student_using_id(id):
    try:
        Srudent_data =student.query.filter_by(s_id=id).first_or_404()
        db.session.commit()
        return jsonify(
                        {
                            's_id' :Srudent_data.s_id,
                            'name':Srudent_data.name,
                            'age':Srudent_data.age,
                            'email':Srudent_data.email,
            } )
    except Exception as e:
        return  {"code": 404 ,"error": e.args}
  

@app.route('/update_student/<id>/',methods=['PUT'])
def update_student(id):
    # data=request.get_json()
    
    # Srudent_data =student.query.filter_by(s_id=id).first_or_404()
    try:
        id =student.query.filter_by(s_id=id).first_or_404()
        # id = student.query.get(id)
        # print(Srudent_data)
        if id is None:
            return {"msg": "id not present"}
        else :
            s_id = request.json['s_id']
            name = request.json['name']
            age = request.json['age']
            email = request.json['email']
            # id.s_id = s_id
            id.name = name
            id.age = age
            id.email = email 
            db.session.add(id)
            db.session.commit()
            return jsonify({"success": True, "response": "Student Details updated"})
            # return jsonify([
            #         {
            #             's_id' :Srudent_data.s_id,
            #             'name':Srudent_data.name,
            #             'age':Srudent_data.age,
            #             'email':Srudent_data.email
            #         } ])
    except Exception as e:
        return jsonify({"error": e.args})

@app.route('/delete_student/<id>/',methods=['DELETE'])
def delete_student(id):
    try:
        Srudent_data =student.query.filter_by(s_id=id).first_or_404()
        db.session.delete(Srudent_data)
        db.session.commit()
        return {
            'success':'Data Delete Successfully'
        }
    except Exception as e:
        return  {"code": 404 ,"error": e.args}

if __name__ == '__main__':
    db.create_all()
    app.run(debug = True)