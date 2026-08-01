from faker import Faker

from .models import User, Workout
from .extensions import db

fake = Faker()

def seed_database():

    Workout.query.delete()
    User.query.delete()

    user = User(username="demo")
    user.password = "password123"

    db.session.add(user)
    db.session.commit()

    for _ in range(10):
        workout = Workout(
            exercise=fake.random_element(
                elements=[
                    "Bench Press",
                    "Squats",
                    "Deadlift",
                    "Pull Ups",
                    "Running",
                    "Cycling"
                ]
            ),
            duration=fake.random_int(min=20, max=90),
            sets=fake.random_int(min=3, max=5),
            reps=fake.random_int(min=8, max=15),
            notes=fake.sentence(),
            user_id=user.id
        )

        db.session.add(workout)

    db.session.commit()

    print("Database seeded successfully.")

from app import create_app

app = create_app()

with app.app_context():
    seed_database()
