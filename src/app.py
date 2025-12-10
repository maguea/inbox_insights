# app.py Tolu Kolade Sept 29, 2025
# This is the main entry point for the flask project. 
# it runs the flask app and defines the port
# 

from src.web_flask.web import app

if __name__ == '__main__':
    app.run(port=5000) 
    