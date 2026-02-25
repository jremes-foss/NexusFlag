from app.core.db import engine, Base, SessionLocal
from app.models.user import User
from app.models.challenge import Challenge, Category, Submission, Difficulty

try:
    from app.core.security import get_password_hash
except ImportError:
    def get_password_hash(password): return f"hashed_{password}"

def seed_data():
    print("[!] Checking database schema...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    if db.query(Category).first():
        print("[!] Database already contains data. Skipping seed to prevent duplicates.")
        db.close()
        return

    try:
        print("[!] Seeding categories...")
        web = Category(name="Web Exploitation")
        crypto = Category(name="Cryptography")
        pwn = Category(name="Binary Exploitation")
        db.add_all([web, crypto, pwn])
        db.commit()

        print("[!] Seeding users...")
        admin = User(
            username="admin", 
            email="admin@nexusflag.com", 
            hashed_password=get_password_hash("admin123"), 
            is_admin=True
        )
        player = User(
            username="player1", 
            email="player@example.com", 
            hashed_password=get_password_hash("player123"),
            score=0
        )
        db.add_all([admin, player])

        print("[!] Seeding challenges...")
        c1 = Challenge(
            title="Inspect Me",
            description="I hid the flag in the HTML comments. Can you find it?",
            flag="NEXUS{v1ew_sourc3_is_k3y}",
            points=50,
            difficulty=Difficulty.EASY,
            category_id=web.id
        )
        
        c2 = Challenge(
            title="Caesar's Secret",
            description="Eby bqr phat vf: ARKHU{pelcgb_vf_sha}",
            flag="NEXUS{crypto_is_fun}",
            points=100,
            difficulty=Difficulty.MEDIUM,
            category_id=crypto.id
        )

        db.add_all([c1, c2])
        db.commit()
        print("[✓] Database seeded successfully!")

    except Exception as e:
        print(f"[x] Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
