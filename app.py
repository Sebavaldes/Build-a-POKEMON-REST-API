from flask import Flask, jsonify, request
from flask_migrate import Migrate
from models import (
    db,
    Usuario,
    Pokemon,
    Favorito,
    Habilidad,
    PokemonHabilidad,
    Estadistica,
)

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
db.init_app(app)
migrate = Migrate(app, db)


@app.route("/")
def home():
    return "Hello Flask App PT 41"


# Crear un nuevo Pokemon
@app.route("/pokemon", methods=["POST"])
def create_pokemon():
    nombre = request.json.get("nombre")
    tipo = request.json.get("tipo")

    if not nombre:
        return jsonify({"message": "El nombre del Pokemon es requerido"}), 400

    pokemon = Pokemon(nombre=nombre, tipo=tipo)
    db.session.add(pokemon)
    db.session.commit()

    return jsonify({"message": "Pokemon creado exitosamente"}), 201


# Obtener todos los Pokemons
@app.route("/pokemon", methods=["GET"])
def get_all_pokemon():
    pokemons = Pokemon.query.all()
    result = []
    for pokemon in pokemons:
        pokemon_data = {
            "id": pokemon.id,
            "nombre": pokemon.nombre,
            "tipo": pokemon.tipo,
        }
        result.append(pokemon_data)
    return jsonify(result), 200


# Obtener un Pokemon por su ID
@app.route("/pokemon/<int:pokemon_id>", methods=["GET"])
def get_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        pokemon_data = {
            "id": pokemon.id,
            "nombre": pokemon.nombre,
            "tipo": pokemon.tipo,
        }
        return jsonify(pokemon_data), 200
    else:
        return jsonify({"message": "Pokemon no encontrado"}), 404


# Eliminar un Pokemon por su ID
@app.route("/pokemon/<int:pokemon_id>", methods=["DELETE"])
def delete_pokemon(pokemon_id):
    pokemon = Pokemon.query.get(pokemon_id)
    if pokemon:
        db.session.delete(pokemon)
        db.session.commit()
        return jsonify({"message": "Pokemon eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Pokemon no encontrado"}), 404


@app.route("/usuarios", methods=["POST"])
def create_usuario():
    nombre_usuario = request.json.get("nombre_usuario")
    email = request.json.get("email")
    password = request.json.get("password")

    if not nombre_usuario or not email or not password:
        return jsonify({"message": "Todos los campos son requeridos"}), 400

    usuario = Usuario(nombre_usuario=nombre_usuario, email=email, password=password)
    db.session.add(usuario)
    db.session.commit()

    return jsonify({"message": "Usuario creado exitosamente"}), 201


# Obtener todos los usuarios
@app.route("/usuarios", methods=["GET"])
def get_usuarios():
    usuarios = Usuario.query.all()
    result = []
    for usuario in usuarios:
        usuario_data = {
            "id": usuario.id,
            "nombre_usuario": usuario.nombre_usuario,
            "email": usuario.email,
        }
        result.append(usuario_data)
    return jsonify(result), 200


# Obtener un usuario por su ID
@app.route("/usuarios/<int:usuario_id>", methods=["GET"])
def get_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        usuario_data = {
            "id": usuario.id,
            "nombre_usuario": usuario.nombre_usuario,
            "email": usuario.email,
        }
        return jsonify(usuario_data), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404


# Eliminar un usuario por su ID
@app.route("/usuarios/<int:usuario_id>", methods=["DELETE"])
def delete_usuario(usuario_id):
    usuario = Usuario.query.get(usuario_id)
    if usuario:
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({"message": "Usuario eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Usuario no encontrado"}), 404


@app.route("/habilidades", methods=["GET"])
def get_all_habilidades():
    habilidades = Habilidad.query.all()
    result = []
    for habilidad in habilidades:
        habilidad_data = {
            "id": habilidad.id,
            "nombre": habilidad.nombre,
            "descripcion": habilidad.descripcion,
        }
        result.append(habilidad_data)
    return jsonify(result), 200


@app.route("/favorites", methods=["POST"])
def add_favorite():
    usuario_id = request.json.get("usuario_id")
    pokemon_id = request.json.get("pokemon_id")

    if usuario_id is None or pokemon_id is None:
        return jsonify({"message": "Usuario ID y Pokemon ID son requeridos"}), 400

    favorito = Favorito(usuario_id=usuario_id, pokemon_id=pokemon_id)
    db.session.add(favorito)
    db.session.commit()

    return jsonify({"message": "Favorito agregado exitosamente"}), 201


# Eliminar un favorito
@app.route("/favorites/<int:favorito_id>", methods=["DELETE"])
def delete_favorite(favorito_id):
    favorito = Favorito.query.get(favorito_id)
    if favorito:
        db.session.delete(favorito)
        db.session.commit()
        return jsonify({"message": "Favorito eliminado exitosamente"}), 200
    else:
        return jsonify({"message": "Favorito no encontrado"}), 404


@app.route("/pokemon_habilidades", methods=["POST"])
def create_pokemon_habilidad():
    pokemon_id = request.json.get("pokemon_id")
    habilidad_id = request.json.get("habilidad_id")

    if not pokemon_id or not habilidad_id:
        return (
            jsonify(
                {"message": "Se requiere el ID del Pokemon y el ID de la Habilidad"}
            ),
            400,
        )

    pokemon_habilidad = PokemonHabilidad(
        pokemon_id=pokemon_id, habilidad_id=habilidad_id
    )
    db.session.add(pokemon_habilidad)
    db.session.commit()

    return jsonify({"message": "Relación PokemonHabilidad creada exitosamente"}), 201


# Obtener todas las relaciones PokemonHabilidad
@app.route("/pokemon_habilidades", methods=["GET"])
def get_pokemon_habilidades():
    pokemon_habilidades = PokemonHabilidad.query.all()
    result = []
    for ph in pokemon_habilidades:
        pokemon_habilidad_data = {
            "id": ph.id,
            "pokemon_id": ph.pokemon_id,
            "habilidad_id": ph.habilidad_id,
        }
        result.append(pokemon_habilidad_data)
    return jsonify(result), 200


# Eliminar una relación PokemonHabilidad por su ID
@app.route("/pokemon_habilidades/<int:pokemon_habilidad_id>", methods=["DELETE"])
def delete_pokemon_habilidad(pokemon_habilidad_id):
    pokemon_habilidad = PokemonHabilidad.query.get(pokemon_habilidad_id)
    if pokemon_habilidad:
        db.session.delete(pokemon_habilidad)
        db.session.commit()
        return (
            jsonify({"message": "Relación PokemonHabilidad eliminada exitosamente"}),
            200,
        )
    else:
        return jsonify({"message": "Relación PokemonHabilidad no encontrada"}), 404


# Crear una estadística
@app.route("/estadisticas", methods=["POST"])
def create_estadistica():
    pokemon_id = request.json.get("pokemon_id")
    tipo_estadistica = request.json.get("tipo_estadistica")
    valor = request.json.get("valor")

    if not pokemon_id or not tipo_estadistica or valor is None:
        return (
            jsonify(
                {
                    "message": "Se requiere el ID del Pokemon, tipo de estadística y valor"
                }
            ),
            400,
        )

    estadistica = Estadistica(
        pokemon_id=pokemon_id, tipo_estadistica=tipo_estadistica, valor=valor
    )
    db.session.add(estadistica)
    db.session.commit()

    return jsonify({"message": "Estadística creada exitosamente"}), 201


# Obtener todas las estadísticas
@app.route("/estadisticas", methods=["GET"])
def get_estadisticas():
    estadisticas = Estadistica.query.all()
    result = []
    for estadistica in estadisticas:
        estadistica_data = {
            "id": estadistica.id,
            "pokemon_id": estadistica.pokemon_id,
            "tipo_estadistica": estadistica.tipo_estadistica,
            "valor": estadistica.valor,
        }
        result.append(estadistica_data)
    return jsonify(result), 200


# Eliminar una estadística por su ID
@app.route("/estadisticas/<int:estadistica_id>", methods=["DELETE"])
def delete_estadistica(estadistica_id):
    estadistica = Estadistica.query.get(estadistica_id)
    if estadistica:
        db.session.delete(estadistica)
        db.session.commit()
        return jsonify({"message": "Estadística eliminada exitosamente"}), 200
    else:
        return jsonify({"message": "Estadística no encontrada"}), 404


if __name__ == "__main__":
    app.run(host="localhost", port=5000)
