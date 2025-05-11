from flask import Flask, render_template, request, jsonify
from models import db, Performance, Experience, User
import os

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        @app.route("/")
        def index():
            years = sorted(set(p.year for p in Performance.query.all()))
            return render_template("index.html", years=years)

        @app.route("/year/<int:year>")
        def lineup(year):
            performances = Performance.query.filter_by(year=year).order_by(Performance.day, Performance.stage).all()
            return render_template("lineup.html", year=year, performances=performances)

        USER_ID = 1

        @app.route("/api/experience/<int:performance_id>", methods=["POST"])
        def update_experience(performance_id):
            data = request.get_json()
            viewing_status = data.get("viewing_status")

            experience = Experience.query.filter_by(user_id=USER_ID, performance_id=performance_id).first()

            if not experience:
                experience = Experience(user_id=USER_ID, performance_id=performance_id)
                db.session.add(experience)

            experience.viewing_status = viewing_status
            if viewing_status != "watched":
                experience.rating = None

            db.session.commit()
            return jsonify({"success": True})

        @app.route("/api/experience/<int:performance_id>/rating", methods=["POST"])
        def update_rating(performance_id):
            data = request.get_json()
            rating = data.get("rating")

            experience = Experience.query.filter_by(user_id=USER_ID, performance_id=performance_id).first()

            if not experience or experience.viewing_status != "watched":
                return jsonify({"error": "Can't rate unless watched"}), 400

            experience.rating = rating
            db.session.commit()
            return jsonify({"success": True})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
