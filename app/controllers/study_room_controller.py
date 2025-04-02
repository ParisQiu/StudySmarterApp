# app/controllers/study_room_controller.py
from flask import request, jsonify
from app.models import StudyRoom
from app import db
# Optionally, uncomment the following line if you want to check for the creator's existence.
# from app.models.user import User

def create_study_room():
    """
    Endpoint for creating a new study room.
    Expects JSON with 'name', 'capacity', and 'creator_id'.
    Optionally accepts 'description'.

    Enhancements:
      - Validates that 'name' is not empty.
- Validates that 'capacity' and 'creator_id' are integers.
- Optionally checks that capacity is a positive number.
- (Optional) Checks that the creator exists.
    """
    try:
        data = request.get_json()
        required_fields = ['name', 'capacity', 'creator_id']
        if not data or not all(field in data for field in required_fields):
            return jsonify({'message': 'Missing required fields'}), 400

        # Validate and sanitize input values
        name = data.get('name', '').strip()
        if not name:
            return jsonify({'message': 'Study room name cannot be empty'}), 400

        try:
            capacity = int(data.get('capacity'))
        except (ValueError, TypeError):
            return jsonify({'message': 'Capacity must be an integer'}), 400

        if capacity <= 0:
            return jsonify({'message': 'Capacity must be greater than zero'}), 400

        try:
            creator_id = int(data.get('creator_id'))
        except (ValueError, TypeError):
            return jsonify({'message': 'Creator ID must be an integer'}), 400

        # Optional: Verify that the creator exists
        # user = User.query.get(creator_id)
        # if not user:
        #     return jsonify({'message': 'Creator (user) not found'}), 404

        description = data.get('description')
        if description:
            description = description.strip()

        # Create and commit the new study room
        new_room = StudyRoom(
            name=name,
            capacity=capacity,
            creator_id=creator_id,
            description=description
        )
        db.session.add(new_room)
        db.session.commit()

        return jsonify({'message': 'Study room created', 'room_id': new_room.room_id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Creation failed', 'error': str(e)}), 500

def get_study_room(id):
    """
Endpoint to fetch a specific study room by its ID.
    """
    try:
        room = StudyRoom.query.get(id)
        if not room:
            return jsonify({'message': 'Room not found'}), 404
        room_data = {
            'room_id': room.room_id,
            'name': room.name,
            'description': room.description,
            'capacity': room.capacity,
            'creator_id': room.creator_id
        }
        return jsonify(room_data), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching room', 'error': str(e)}), 500

def get_all_study_rooms():
    """
Endpoint to fetch all study rooms.
    """
    try:
        rooms = StudyRoom.query.all()
        rooms_data = [{
            'room_id': room.room_id,
            'name': room.name,
            'capacity': room.capacity
        } for room in rooms]
        return jsonify(rooms_data), 200
    except Exception as e:
        return jsonify({'message': 'Error fetching rooms', 'error': str(e)}), 500
        