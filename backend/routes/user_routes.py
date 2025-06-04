from flask import Blueprint, jsonify, request
from backend.__init__ import db # Importa db de la inicialización de Flask
from backend.models.user import User
from backend.models.role import Role
from backend.models.user import user_roles # Para la tabla intermedia

user_bp = Blueprint('users', __name__, url_prefix='/api/users')

@user_bp.route('/', methods=['GET'])
def get_users():
    users = db.session.execute(db.select(User)).scalars().all()
    # No devuelvas contraseñas en una aplicación real
    return jsonify([{'user_id': user.user_id, 'username': user.username} for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password') # ¡Recuerda hashear en producción!

    if not username or not password:
        return jsonify({'message': 'Username and password are required'}), 400

    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.user_id, 'username': new_user.username}), 201

# Puedes añadir rutas para roles si las necesitas
@user_bp.route('/roles', methods=['GET'])
def get_roles():
    roles = db.session.execute(db.select(Role)).scalars().all()
    return jsonify([{'role_id': role.role_id, 'role_name': role.role_name} for role in roles])

@user_bp.route('/roles', methods=['POST'])
def create_role():
    data = request.get_json()
    role_name = data.get('role_name')
    if not role_name:
        return jsonify({'message': 'Role name is required'}), 400
    new_role = Role(role_name=role_name)
    db.session.add(new_role)
    db.session.commit()
    return jsonify({'role_id': new_role.role_id, 'role_name': new_role.role_name}), 201