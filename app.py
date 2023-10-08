from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


# Modelo SQLAlchemy
class Item(db.Model):
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(200))

    def __init__(self, name, description):
        self.name = name
        self.description = description

    def as_dict(self):
        return {'id': self.id, 'name': self.name, 'description': self.description}


# Operaciones CRUD
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    item_list = [item.as_dict() for item in items]
    return jsonify({'items': item_list}), 200


@app.route('/items/<int:id>', methods=['GET'])
def get_item(id):
    item = Item.query.get_or_404(id)
    return jsonify({'item': item.as_dict()}), 200


@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    item = Item(name=data['name'], description=data['description'])
    db.session.add(item)
    db.session.commit()
    return jsonify({'item': item.as_dict(), 'message': 'Item created successfully'}), 201


@app.route('/items/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return jsonify({'item': item.as_dict(), 'message': 'Item updated successfully'}), 200


@app.route('/items/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item deleted successfully'}), 200
