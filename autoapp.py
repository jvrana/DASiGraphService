from flask import Flask
from DASiGraph import app

if __name__ == "__main__":
    myapp = app.create_app("config")
    myapp.run(debug=True)