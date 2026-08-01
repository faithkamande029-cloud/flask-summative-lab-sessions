from marshmallow import Schema, fields, validate

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    exercise = fields.Str(required=True)
    duration = fields.Int(required=True)
    sets = fields.int()
    reps = fields.Int()
    notes = fields.Str()
    user_id = fields.Int(dump_only=True)

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)

workout_schema = WorkoutSchema()
workout_schema = WorkoutSchema(many=True)

user_schema = UserSchema()
user_schema = UserSchema(many=True)
