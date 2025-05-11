import os
import json
from datetime import datetime
from app import app
from models import db, Performance

DATA_DIR = './data'

def get_day_name(date_string):
    """Convert date string to weekday name (e.g., Thursday)"""
    dt = datetime.strptime(date_string, "%Y-%m-%d %H:%M")
    return dt.strftime("%A")

def import_performances():
    with app.app_context():
        for filename in os.listdir(DATA_DIR):
            if filename.endswith('.json'):
                year = int(''.join(filter(str.isdigit, filename)))
                filepath = os.path.join(DATA_DIR, filename)

                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                for location in data.get('locations', []):
                    stage = location.get('name')

                    for event in location.get('events', []):
                        artist = event.get('name')
                        start_time = event.get('start')
                        day = get_day_name(start_time)

                        performance = Performance(
                            artist=artist,
                            stage=stage,
                            day=day,
                            year=year
                        )
                        db.session.add(performance)

        db.session.commit()
        print("🎉 Data imported successfully!")

if __name__ == "__main__":
    import_performances()
