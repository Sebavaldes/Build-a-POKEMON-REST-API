from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Usuario(db.Model):
    __tablename__ = "usuario"
    id = db.Column(db.Integer, primary_key=True)
    nombre_usuario = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    password = db.Column(db.String(250), nullable=False)
    favoritos = db.relationship("Favorito")


class Pokemon(db.Model):
    __tablename__ = "pokemon"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    tipo = db.Column(db.String(250))
    habilidades = db.relationship("Habilidad", secondary="pokemon_habilidad")
    estadisticas = db.relationship("Estadistica")


class Favorito(db.Model):
    __tablename__ = "favorito"
    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey("usuario.id"))
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"))
    usuario = db.relationship(Usuario)
    pokemon = db.relationship(Pokemon)


class Habilidad(db.Model):
    __tablename__ = "habilidad"
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(250), nullable=False)
    descripcion = db.Column(db.String(250))


class PokemonHabilidad(db.Model):
    __tablename__ = "pokemon_habilidad"
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"))
    habilidad_id = db.Column(db.Integer, db.ForeignKey("habilidad.id"))


class Estadistica(db.Model):
    __tablename__ = "estadistica"
    id = db.Column(db.Integer, primary_key=True)
    pokemon_id = db.Column(db.Integer, db.ForeignKey("pokemon.id"))
    tipo_estadistica = db.Column(db.String(250), nullable=False)
    valor = db.Column(db.Integer)
