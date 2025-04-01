from flask import Flask

def create_app():
    app = Flask(__name__)

    from .routes import calculator, derivada
    app.register_blueprint(calculator)
    app.register_blueprint(derivada)

    return app
