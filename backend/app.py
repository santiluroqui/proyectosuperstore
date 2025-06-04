from backend.__init__ import create_app, db # Importa create_app y db de tu __init__.py
from backend.models.order import Order, Base # Necesario para la migración
from backend.models.user import User
from backend.models.role import Role

# Crea la aplicación y obtiene la sesión y la Base
app, session, Base_obj = create_app()

# Para servir los archivos estáticos del frontend desde Flask
from flask import send_from_directory

@app.route('/')
def serve_frontend():
    return send_from_directory('../frontend', 'index.html')

@app.route('/<path:path>')
def serve_frontend_assets(path):
    return send_from_directory('../frontend', path)

if __name__ == '__main__':
    # Este bloque se ejecuta cuando corres `python app.py`
    # ¡No necesitas create_database.py si usas este enfoque!
    print("Iniciando la aplicación Flask...")
    app.run(debug=True) # debug=True es solo para desarrollo