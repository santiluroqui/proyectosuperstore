import os

class Config:
    # Obtiene la URL de la base de datos de una variable de entorno
    # (¡Esto es crucial para el despliegue en la nube!)
    # Si no está definida (ej. en desarrollo local), usa una URL por defecto.
    # REEMPLAZA 'TU_URL_DE_ELEPHANTSQL' con la URL que obtuviste de ElephantSQL.
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:123456@localhost:5432/superstore'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'una_clave_secreta_muy_segura_aqui_para_flask'