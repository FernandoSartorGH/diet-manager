from database import db

class Diet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(80), unique=True, nullable=False)
    descricao = db.Column(db.String(80), nullable=False)
    data = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(80), nullable=False)