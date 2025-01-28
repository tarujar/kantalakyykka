import sys
import os

# Add the parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app
from seeders.player_seeder import seed_players

def run_seeders():
    with app.app_context():
        print("Starting database seeding...")
        seed_players()
        print("Database seeding completed!")

if __name__ == "__main__":
    run_seeders()
