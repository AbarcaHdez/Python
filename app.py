from flask import Flask
from flasgger import Swagger
from routes.usuarios import usuarios_bp

app = Flask(__name__)

swagger = Swagger(app)

app.register_blueprint(usuarios_bp)

if __name__ == "__main__":
    app.run(debug=True)