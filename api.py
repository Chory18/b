from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, Categoria, Producto, Usuario
from .utils import get_password_hash, verify_password

api = Blueprint('api', __name__)

# Rutas de autenticación
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    usuario = Usuario.query.filter_by(correo=data.get('correo')).first()
    
    if not usuario or not verify_password(data.get('contraseña'), usuario.contraseña):
        return jsonify({"msg": "Correo o contraseña incorrectos"}), 401
    
    access_token = create_access_token(identity=usuario.id)
    return jsonify(access_token=access_token)

# Rutas de Categorías
@api.route('/categorias', methods=['GET'])
@jwt_required()
def get_categorias():
    categorias = Categoria.query.all()
    return jsonify([{"id": c.id, "nombre": c.nombre} for c in categorias])

@api.route('/categorias/<int:categoria_id>', methods=['GET'])
@jwt_required()
def get_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    return jsonify({"id": categoria.id, "nombre": categoria.nombre})

@api.route('/categorias', methods=['POST'])
@jwt_required()
def create_categoria():
    data = request.get_json()
    categoria = Categoria(nombre=data['nombre'])
    db.session.add(categoria)
    db.session.commit()
    return jsonify({"id": categoria.id, "nombre": categoria.nombre}), 201

@api.route('/categorias/<int:categoria_id>', methods=['PUT'])
@jwt_required()
def update_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    data = request.get_json()
    categoria.nombre = data['nombre']
    db.session.commit()
    return jsonify({"id": categoria.id, "nombre": categoria.nombre})

@api.route('/categorias/<int:categoria_id>', methods=['DELETE'])
@jwt_required()
def delete_categoria(categoria_id):
    categoria = Categoria.query.get_or_404(categoria_id)
    db.session.delete(categoria)
    db.session.commit()
    return '', 204

# Rutas de Productos
@api.route('/productos', methods=['GET'])
@jwt_required()
def get_productos():
    productos = Producto.query.all()
    return jsonify([{
        "id": p.id,
        "nombre": p.nombre,
        "precio": float(p.precio),
        "categoria_id": p.categoria_id
    } for p in productos])

@api.route('/productos/<int:producto_id>', methods=['GET'])
@jwt_required()
def get_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    return jsonify({
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "categoria_id": producto.categoria_id
    })

@api.route('/productos', methods=['POST'])
@jwt_required()
def create_producto():
    data = request.get_json()
    if data.get('categoria_id'):
        categoria = Categoria.query.get_or_404(data['categoria_id'])
    producto = Producto(
        nombre=data['nombre'],
        precio=data['precio'],
        categoria_id=data.get('categoria_id')
    )
    db.session.add(producto)
    db.session.commit()
    return jsonify({
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "categoria_id": producto.categoria_id
    }), 201

@api.route('/productos/<int:producto_id>', methods=['PUT'])
@jwt_required()
def update_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    data = request.get_json()
    if data.get('categoria_id'):
        categoria = Categoria.query.get_or_404(data['categoria_id'])
    
    producto.nombre = data['nombre']
    producto.precio = data['precio']
    producto.categoria_id = data.get('categoria_id')
    db.session.commit()
    return jsonify({
        "id": producto.id,
        "nombre": producto.nombre,
        "precio": float(producto.precio),
        "categoria_id": producto.categoria_id
    })

@api.route('/productos/<int:producto_id>', methods=['DELETE'])
@jwt_required()
def delete_producto(producto_id):
    producto = Producto.query.get_or_404(producto_id)
    db.session.delete(producto)
    db.session.commit()
    return '', 204

# Rutas de Usuarios
@api.route('/usuarios', methods=['GET'])
@jwt_required()
def get_usuarios():
    usuarios = Usuario.query.all()
    return jsonify([{
        "id": u.id,
        "nombre": u.nombre,
        "correo": u.correo,
        "creado_en": u.creado_en.isoformat()
    } for u in usuarios])

@api.route('/usuarios/<int:usuario_id>', methods=['GET'])
@jwt_required()
def get_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "creado_en": usuario.creado_en.isoformat()
    })

@api.route('/usuarios', methods=['POST'])
def create_usuario():
    data = request.get_json()
    if Usuario.query.filter_by(correo=data['correo']).first():
        return jsonify({"msg": "Correo ya registrado"}), 400
    
    usuario = Usuario(
        nombre=data['nombre'],
        correo=data['correo'],
        contraseña=get_password_hash(data['contraseña'])
    )
    db.session.add(usuario)
    db.session.commit()
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "creado_en": usuario.creado_en.isoformat()
    }), 201

@api.route('/usuarios/<int:usuario_id>', methods=['PUT'])
@jwt_required()
def update_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    data = request.get_json()
    
    if 'correo' in data and data['correo'] != usuario.correo:
        if Usuario.query.filter_by(correo=data['correo']).first():
            return jsonify({"msg": "Correo ya registrado"}), 400
    
    usuario.nombre = data.get('nombre', usuario.nombre)
    usuario.correo = data.get('correo', usuario.correo)
    if 'contraseña' in data:
        usuario.contraseña = get_password_hash(data['contraseña'])
    
    db.session.commit()
    return jsonify({
        "id": usuario.id,
        "nombre": usuario.nombre,
        "correo": usuario.correo,
        "creado_en": usuario.creado_en.isoformat()
    })

@api.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
@jwt_required()
def delete_usuario(usuario_id):
    usuario = Usuario.query.get_or_404(usuario_id)
    db.session.delete(usuario)
    db.session.commit()
    return '', 204 