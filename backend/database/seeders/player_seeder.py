from app.main import db
from app.models.models import Player
import random
from datetime import datetime, timezone

# Common Finnish first names and last names
first_names = [
    "Mikko", "Jukka", "Pekka", "Timo", "Sami", "Antti", "Juha", "Matti", "Ville", "Jani",
    "Maria", "Anna", "Laura", "Johanna", "Sari", "Riikka", "Tarja", "Liisa", "Tiina", "Hanna"
]

last_names = [
    "Korhonen", "Virtanen", "Mäkinen", "Nieminen", "Mäkelä", "Hämäläinen", "Laine",
    "Heikkinen", "Koskinen", "Järvinen", "Lehtonen", "Lehtinen", "Saarinen", "Salminen"
]

email_domains = ["gmail.com", "outlook.com", "hotmail.com", "yahoo.com"]

def generate_mock_players(count=50):
    """Generate mock player data"""
    players = []
    used_emails = set()
    
    for _ in range(count):
        first_name = random.choice(first_names)
        last_name = random.choice(last_names)
        
        # Create unique email
        while True:
            email_domain = random.choice(email_domains)
            email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"
            if email not in used_emails:
                used_emails.add(email)
                break
        
        player = Player(
            name=f"{first_name} {last_name}",
            email=email,
            created_at=datetime.now(timezone.utc),
            gdpr_consent=True  # Set GDPR consent to True for seeded players
        )
        players.append(player)
    
    return players

def seed_players():
    """Seed the database with mock players"""
    try:
        players = generate_mock_players()
        db.session.bulk_save_objects(players)
        db.session.commit()
        print(f"Successfully seeded {len(players)} players")
    except Exception as e:
        db.session.rollback()
        print(f"Error seeding players: {e}")

if __name__ == "__main__":
    seed_players()
