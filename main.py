from blueprints.Simon_blueprints import simon_server_blueprint
from flask import *

def  create_app():
    app = Flask("Simon-backend")  # Start the Flask service application.
    app.register_blueprint(simon_server_blueprint)
#    app.run(host='0.0.0.0', port=8079, debug=True)
    return app

if __name__ == "__main__":
    create_app()
    app.run(host='0.0.0.0', port=8079, debug=True)
