from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Float
import os


app = Flask(__name__)                                     # these __x__ means thi particular app will take
basedir = os.path.abspath(os.path.dirname(__file__))      # its name form the name of the script
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'planets.db')  # you can changfe these to hard coded string


db = SQLAlchemy(app)


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
    Earth = Planet(planet_name='Earth', planet_type='Class M', home_star='Sol', mass=5.972e24, radius=3959, distance=35.98e6)
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
        return jsnify(message="Welcome " + name + ", you are old enoyugh!")


# database models

class User(db.Model):
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)


class Planet(db.Model):
    planet_id = Column(Integer, primary_key=True)
    planer_name = Column(String)
    planmet_type = Column(String)
    home_star = Column(String)
    mass = Column(Float)
    radus = Column(Float)
    distance =  Column(Float)




if __name__ == '__main__':    # these if pythin for scripting
    app.run()                 # all it does is to give an entry point