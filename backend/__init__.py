from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from backend.config import Config # Importa tu configuración
from backend.models.order import Base # Importa Base de uno de tus modelos (son la misma Base)
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db = SQLAlchemy() # Inicializa SQLAlchemy (lo usaremos con Flask)

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app) # Inicializa db con la aplicación Flask

    # Crea el engine y la sesión de SQLAlchemy directamente aquí para la migración
    # Esto es independiente de Flask-SQLAlchemy para la creación de tablas
    engine = create_engine(config_class.SQLALCHEMY_DATABASE_URI)
    Session = sessionmaker(bind=engine)
    session = Session()

    # Importa y registra tus blueprints (rutas)
    from backend.routes.order_routes import order_bp
    from backend.routes.user_routes import user_bp
    app.register_blueprint(order_bp)
    app.register_blueprint(user_bp)

    # Contexto de aplicación para manejar la creación de tablas
    with app.app_context():
        # Crea todas las tablas definidas en Base.metadata si no existen
        Base.metadata.create_all(engine) # Usa el engine directo de SQLAlchemy

    return app, session, Base # Devuelve la app, la sesión y la Base