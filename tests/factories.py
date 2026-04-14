import factory
from app.models.user import User
from app.models.challenge import Category, Challenge, Submission, Difficulty

class CategoryFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Category
        sqlalchemy_session_persistence = "commit"
    name = factory.Sequence(lambda n: f"Category {n}")

class ChallengeFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Challenge
        sqlalchemy_session_persistence = "commit"
    title = factory.Sequence(lambda n: f"Challenge {n}")
    description = "Test description"
    points = 100
    difficulty = Difficulty.MEDIUM
    flag = "CTF{test_flag}"
    category = factory.SubFactory(CategoryFactory)

class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session_persistence = "commit"

    username = factory.Sequence(lambda n: f"user_{n}")
    # Add this line to satisfy the NOT NULL constraint
    email = factory.Sequence(lambda n: f"user_{n}@example.com")
    hashed_password = "fake_hashed_password"
    score = 0
