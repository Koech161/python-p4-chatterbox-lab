from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate

from models import db, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

@app.route('/messages', methods=['GET', 'POST'])
def messages():

    if request.method == 'GET':
        messages = Message.query.order_by(Message.created_at.asc()).all()
        message_list = [message.to_dict() for message in messages]
        return jsonify(message_list), 200
    
    elif request.method == 'POST':
        data = request.json
        body = data.get('body')
        username = data.get('username')
        if not body or not username:
            return jsonify({"error": "Body and username are required"}), 400
        new_message = Message(body=body, username=username)
        db.session.add(new_message)
        db.session.commit()
        return jsonify(new_message.to_dict()), 201 
        # body = request.form.get('body')
        # username = request.form.get('username')
        # if not body or not username:
        #     return jsonify({"error": "Body and username are required"}), 400
        # new_message = Message(body=body, username=username)
        # db.session.add(new_message)
        # db.session.commit()
        # return jsonify(new_message.to_dict()),201
        

@app.route('/messages/<int:id>', methods=['PATCH', 'DELETE'])
def messages_by_id(id):
    message = Message.query.filter(Message.id == id).first()
    if request.method == 'PATCH':
        for attr in request.json:
            setattr(message, attr, request.json.get(attr))
        
        db.session.commit()
        return jsonify(message.to_dict()), 200

    elif request.method == 'DELETE':
        db.session.delete(message)
        db.session.commit()
        response_body = {
            "message": "message deleted successfuly."
        }
        return jsonify(response_body), 200

if __name__ == '__main__':
    app.run(port=5555)
