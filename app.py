from flask import Flask, request, jsonify, render_template

from models import db, connect_db, Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcake_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "oh-so-secret"

## need to use these 3 lines plus $createdb <db name. when $python seed.py
#connect_db(app)
#app.app_context().push()
#db.create_all()

with app.app_context():
    connect_db(app)
    db.create_all()


@app.route('/')
def index_page():
    """Renders html template that includes some JS - NOT PART OF JSON API!"""
    cupcakes = Cupcake.query.all()
    return render_template('index.html', cupcakes=cupcakes)


@app.route('/api/cupcakes')
def list_cupcakes():
    """Return JSON with all cupcakes"""
    all_cupcakes = [cupcake.serialize() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=all_cupcakes)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    """Returns JSON for one cupcake in particular"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes', methods=["POST"])
def create_cupcake():
    """Creates a new cupcake and returns JSON of that created cupcake"""
    
    data = request.json
    
    new_cupcake = Cupcake(
        flavor = data['flavor'],
        size = data['size'],
        rating = data['rating'],
        image = data['image'] or None)
            
    db.session.add(new_cupcake)
    db.session.commit()
    
    response_json = jsonify(cupcake=new_cupcake.serialize())
    return (response_json, 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["PATCH"])
def update_cupcake(cupcake_id):
    """Updates a particular cupcake and responds w/ JSON of that updated cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.flavor = request.json.get('flavor', cupcake.flavor)
    cupcake.size = request.json.get('size', cupcake.size)
    cupcake.rating = request.json.get('rating', cupcake.rating)
    cupcake.image = request.json.get('image', cupcake.image)
    
    db.session.commit()
    return jsonify(cupcake=cupcake.serialize())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=["DELETE"])
def delete_cupcake(cupcake_id):
    """Deletes a particular cupcake"""
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(message="deleted")
