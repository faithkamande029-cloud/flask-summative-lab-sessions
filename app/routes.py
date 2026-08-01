from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from .models import Workout, User
from .extensions import db

workout_bp = Blueprint("workouts", __name__)

@workout_bp.route("/workouts", methods=["GET"])
@jwt_required()
def get_workouts():

    current_user_id = int(get_jwt_identity())

    page = request.args.get("page", 1, type=int)
    per_page = 5

    pagination = Workout.query.filter_by(
        user_id=current_user_id
    ).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )

    workouts = []

    for workout in pagination.items:
        workouts.append({
            "id": workout.id,
            "exercise": workout.exercise,
            "duration": workout.duration,
            "sets": workout.sets,
            "reps": workout.reps,
            "notes": workout.notes
        })

    return {
        "page": pagination.page,
        "pages": pagination.pages,
        "total": pagination.total,
        "workouts": workouts
    }, 200

@workout_bp.route("/workouts", methods=["POST"])
@jwt_required()
def create_workout():
    data = request.get_json()

    current_user_id = int(get_jwt_identity())

    workout = Workout(
        exercise=data["exercise"],
        duration=data["duration"],
        sets=data.get("sets"),
        reps=data.get("reps"),
        notes=data.get("notes"),
        user_id=current_user_id
    )

    db.session.add(workout)
    db.session.commit()

    return {
        "message": "Workout created successfully.",
        "id": workout.id
    }, 201

@workout_bp.route("/workouts/<int:id>", methods=["GET"])
@jwt_required()
def get_workout(id):

    current_user_id = int(get_jwt_identity())

    workout = Workout.query.filter_by(
        id=id,
        user_id=current_user_id
    ).first()

    if workout is None:
        return {"message": "Workout not found."}, 404

    return {
        "id": workout.id,
        "exercise": workout.exercise,
        "duration": workout.duration,
        "sets": workout.sets,
        "reps": workout.reps,
        "notes": workout.notes
    }, 200

@workout_bp.route("/workouts/<int:id>", methods=["PATCH"])
@jwt_required()
def update_workout(id):

    current_user_id = int(get_jwt_identity())

    workout = Workout.query.filter_by(
        id=id,
        user_id=current_user_id
    ).first()

    if workout is None:
        return {"message": "Workout not found."}, 404

    data = request.get_json()

    workout.exercise = data.get("exercise", workout.exercise)
    workout.duration = data.get("duration", workout.duration)
    workout.sets = data.get("sets", workout.sets)
    workout.reps = data.get("reps", workout.reps)
    workout.notes = data.get("notes", workout.notes)

    db.session.commit()

    return {
        "message": "Workout updated successfully."
    }, 200

@workout_bp.route("/workouts/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_workout(id):

    current_user_id = int(get_jwt_identity())

    workout = Workout.query.filter_by(
        id=id,
        user_id=current_user_id
    ).first()

    if workout is None:
        return {"message": "Workout not found."}, 404

    db.session.delete(workout)
    db.session.commit()

    return {
        "message": "Workout deleted successfully."
    }, 200
