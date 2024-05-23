from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Events, event_schema, events_schema

api = Blueprint('api',__name__, url_prefix='/api')

@api.route('/getdata')
def getdata():
    return {'title': 'Strawberry  festival'}



@api.route('/events', methods = ['POST'])
@token_required
def create_event(current_user_token):
    title = request.json['title']
    event_type = request.json['event_type']
    description = request.json['description']
    location = request.json['location']
    start_time = request.json['start_time']
    end_time = request.json['end_time']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    event = Events(title, event_type, description, location, start_time, end_time, user_token=user_token)

    db.session.add(event)
    db.session.commit()

    response = event_schema.dump(event)
    return jsonify(response)

@api.route('/events', methods = ['GET'])
@token_required
def get_event(current_user_token):
    a_user = current_user_token.token
    events = Events.query.filter_by(user_token = a_user).all()
    response = events_schema.dump(events)
    return jsonify(response)

@api.route('/events/<id>', methods = ['GET'])
@token_required
def get_event_two(current_user_token, id):
    fan = current_user_token.token
    if fan == current_user_token.token:
        event = Events.query.get(id)
        response = event_schema.dump(event)
        return jsonify(response)
    else:
        return jsonify({"message": "Valid Token Required"}),401

# UPDATE endpoint
@api.route('/events/<id>', methods = ['POST','PUT'])
@token_required
def update_book(current_user_token,id):
    event = Events.query.get(id) 
    event.title = request.json['title']
    event.event_type = request.json['event_type']
    event.description = request.json['description']
    event.location = request.json['location']
    event.start_time = request.json['start_time']
    event.end_time = request.json['end_time']
    event.user_token = current_user_token.token

    db.session.commit()
    response = event_schema.dump(event)
    return jsonify(response)


@api.route('/events/<id>', methods = ['DELETE'])
@token_required
def delete_book(current_user_token, id):
    event = Events.query.get(id)
    db.session.delete(event)
    db.session.commit()
    response = event_schema.dump(event)
    return jsonify(response)





    
