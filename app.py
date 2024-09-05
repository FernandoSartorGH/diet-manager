from database import db
from models.diet import Diet
from datetime import datetime
from flask import Flask, request, jsonify
from sqlalchemy.exc import SQLAlchemyError

# app
app = Flask(__name__)

app.config['SECRET_KEY'] = 'my_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)


# routes
@app.route('/diet', methods=['POST'])
def create_diet():
    data = request.json
    name = data.get('nome')
    description = data.get('descricao')
    datetime_str = data.get('data')
    status = data.get('status')

    try:
        datetime_obj = datetime.strptime(datetime_str, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return jsonify({'message': 'Formato de data inválido. Use o formato YYYY-MM-DD HH:MM:SS'}), 400

    if name and description and datetime_str and status:
        diet = Diet(nome=name, descricao=description, data=datetime_obj, status=status)
        try:
            db.session.add(diet)
            db.session.commit()
            return jsonify({'message': 'Dieta cadastrada com sucesso'})

        except SQLAlchemyError as e:
            db.session.rollback()
            return jsonify({'message': 'Erro ao cadastrar dieta', 'error': str(e)}), 500
    return jsonify({'message': 'Dados inválidos'}), 400


@app.route('/diets', methods=['GET'])
def read_diets():
    try:
        diets = Diet.query.all()

        result = [
            {
                'id': diet.id,
                'nome': diet.nome,
                'descricao': diet.descricao,
                'data': diet.data.strftime('%Y-%m-%d %H:%M:%S'),
                'status': diet.status
            }
            for diet in diets
        ]
        if result:
            return jsonify(result)

    except SQLAlchemyError as e:
        return jsonify({'message': 'Erro ao buscar dietas', 'error': str(e)}), 500


@app.route('/diet/<int:id>', methods=['GET'])
def read_diet(id):
    diet = Diet.query.get(id)
    try:
        if diet:
            return jsonify({'Dieta': diet.nome})
        return jsonify({'message': 'Dieta não encontrada'})

    except SQLAlchemyError as e:
        return jsonify({'message': 'Erro ao buscar dietas', 'error': str(e)}), 500


@app.route('/diet/<int:id>', methods=['PUT'])
def update_diet(id):
    data = request.json
    diet = Diet.query.get(id)

    if not diet:
        return jsonify({'Message': 'Dieta não encontrada'})

    try:
        if data.get('nome') and data.get('descricao') and data.get('data') and data.get('status'):
            diet.nome = data.get('nome')
            diet.descricao = data.get('descricao')
            diet.data = datetime.strptime(data.get('data'), '%Y-%m-%d %H:%M:%S')
            diet.status = data.get('status')

            db.session.commit()
            return jsonify({'message': f"Dieta {data.get('nome')} atualizado com sucesso"})

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao atualizar usuário', 'error': str(e)}), 500


@app.route('/diet/<int:id>', methods=['DELETE'])
def delete_diet(id):
    diet = Diet.query.get(id)

    try:
        if diet:
            db.session.delete(diet)
            db.session.commit()
            return jsonify({'message': f"Dieta {diet} deletada com sucesso"})
        return jsonify({'message': 'Dieta não encontrada'}), 404

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'message': 'Erro ao deletar a dieta', 'error': str(e)}), 500


# run
if __name__ == '__main__':
    app.run(debug=True)
