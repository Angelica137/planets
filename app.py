from flask import Flask

app = Flask(__name__) # these __x__ means thi particular app will take
                      # its name form the name of the script
											# you can changfe these to hard coded string

@app.route('/')              # a decorator gives special capabilities to our functions
def hello_world():           # this line defines the route for our endpoint
    return 'Hellow World!'


if __name__ == '__main__':    # these if pythin for scripting
    app.run()                 # all it does is to give an entry point