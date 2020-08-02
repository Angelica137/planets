from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os
from os import environ, path
from dotenv import load_dotenv
from flask_marshmallow import Marshmallow
from flask_jwt_extended import JWTManager, jwt_required, create_access_token
from flask_mail import Mail, Message


app = Flask(__name__)                                     # these __x__ means thi particular app will take
basedir = os.path.abspath(os.path.dirname(__file__))      # its name form the name of the script
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')  # you can changfe these to hard coded string
app.config['JWT_SECRET_KEY'] = environ.get('JWT_SECRET_KEY') # change this for the love of god
app.config['MAIL_SERVER']= environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = environ.get('MAIL_PORT')
app.config['MAIL_USERNAME'] = environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = environ.get('MAIL_USE_TLS')
#app.config['MAIL_USE_SSL'] = environ.get('MAIL_USE_SSL')


db = SQLAlchemy(app)
ma = Marshmallow(app)
jwt = JWTManager(app)
mail = Mail(app)


@app.cli.command('db_create')
def db_create():
    db.create_all()
    print('DB created')


@app.cli.command('db_drop')
def db_drop():
    db.drop_all()
    print('DB dropped')


@app.cli.command('db_seed')
def db_seed():
    mercury = Planet(planet_name='Mercury', planet_type='Class D', home_star='Sol', mass=3.58e23, radius=1516, distance=35.98e6)
    earth = Planet(planet_name='Earth', planet_type='Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=35.98e6)
    venus = Planet(planet_name='Venus', planet_type='Class K', home_star='Sol', mass=4.86e24, radius=1516, distance=35.98e6)

    db.session.add(mercury)
    db.session.add(earth)
    db.session.add(venus)

    test_user = User(first_name='William', last_name='Herschel', email='test@test.com', password='Password')

    db.session.add(test_user)
    db.session.commit()
    print('Database seeded')


@app.route('/')              # a decorator gives special capabilities to our functions
def hello_world():           # this line defines the route for our endpoint
    return 'Hellow World!'


@app.route('/first_json')
def first_json():
    return jsonify(message="Find amazing planets")


@app.route('/url_variables/<string:name>/<int:age>')
def url_vaiables(name: str, age: int):
    if age < 18:
        return jsonify(message="Soz " + name + ", you are not old enough"), 401
    else:
        return jsonify(message="Welcome " + name + ", you are old enoyugh!")


@app.route('/planets', methods=['GET'])
def planets():
    planets_list = Planet.query.all()
    result = planets_schema.dump(planets_list)
    return jsonify(result)


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    test = User.query.filter_by(email=email).first()
    if test:
        return jsonify(message='That email already exists'), 409
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        password = request.form['password']
        user = User(first_name=first_name, last_name=last_name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        return jsonify(message='User created successfully'), 201


@app.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json['email']
        password = request.json['password']
    else:
        email = request.form['email']
        password = request.form['password']

    test = User.query.filter_by(email=email, password=password).first()
    if test:
          access_token = create_access_token(identity=email)
          return jsonify(message='log in sucessful', access_token=access_token)
    else:
          return jsonify(message='Bad email or password'), 401


@app.route('/retrieve_password/<string:email>')
def retrieve_password(email: str):
    user = User.query.filter_by(email=email).first()
    if user:
        msg = Message("your password is" + user.password, sender='amin@planets.com', recipients=[email])
        mail.send(msg)
        return jsonify(message="Password sent to " + email)
    else:
        return jsonify(message='That email does not exist')


# database models

class User(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    planet_id = Column(Integer, primary_key=True)
    planet_name = Column(String)
    planet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radius = Column(Float)
    distance =  Column(Float)


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'first_name', 'last_name', 'email', 'password')


class PlanetSchema(ma.Schema):
    class Meta:
        fields = ('planet_id', 'planet_name', 'planet_type', 'home_star', 'mass', 'radius', 'distance')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


planet_schema = PlanetSchema()
planets_schema = PlanetSchema(many=True)

if __name__ == '__main__':    # these if pythin for scripting
    app.run()                 # all it does is to give an entry point