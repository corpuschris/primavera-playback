from flask import Flask, render_template, request, jsonify
from models import db, Performance, Experience, User
import os


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')

    db.init_app(app)

    with app.app_context():
        db.create_all()

        USER_ID = 1

        @app.route("/")
        def index():
            years = sorted(set(p.year for p in Performance.query.all()))
            experiences = Experience.query.filter_by(user_id=USER_ID).all()
            watched_by_year = {}

            for exp in experiences:
                if exp.viewing_status in ["watched", "glanced"]:
                    perf = Performance.query.get(exp.performance_id)
                    if perf:
                        watched_by_year.setdefault(perf.year, []).append(perf.artist)

            experience_lookup = {}
            for exp in experiences:
                perf = Performance.query.get(exp.performance_id)
                if perf:
                    experience_lookup[perf.artist] = {
                        "status": exp.viewing_status,
                        "rating": exp.rating
                    }

            return render_template(
                "index.html",
                years=years,
                watched_by_year=watched_by_year,
                experience_lookup=experience_lookup
            )

        @app.route("/year/<int:year>")
        def lineup(year):
            performances = Performance.query.filter_by(year=year).order_by(Performance.day, Performance.stage).all()

            experience_entries = Experience.query.filter_by(user_id=USER_ID).all()
            experience_data = {
                exp.performance_id: {
                    "status": exp.viewing_status,
                    "rating": exp.rating
                } for exp in experience_entries
            }

            slogans = {
                2022: "The New Normal",
                2023: "I'll Be Your Mirror",
                2024: "This Is Love",
                2025: "Where Memories Become Music"
            }

            slogan = slogans.get(year, "Primavera Forever")
            theme_class = f"theme-{year}"

            return render_template(
                "lineup.html",
                year=year,
                performances=performances,
                experience_data=experience_data,
                theme_class=theme_class,
                slogan=slogan
            )

        @app.route("/stats")
        def stats():
            experiences = Experience.query.filter_by(user_id=USER_ID).all()
            watched = sum(1 for exp in experiences if exp.viewing_status == "watched")
            glanced = sum(1 for exp in experiences if exp.viewing_status == "glanced")
            skipped = sum(1 for exp in experiences if exp.viewing_status == "skipped")

            return render_template("stats.html", watched=watched, glanced=glanced, skipped=skipped)

        @app.route("/api/experience/<int:performance_id>", methods=["POST"])
        def update_experience(performance_id):
            data = request.get_json()
            viewing_status = data.get("viewing_status")

            experience = Experience.query.filter_by(user_id=USER_ID, performance_id=performance_id).first()

            if not experience:
                experience = Experience(user_id=USER_ID, performance_id=performance_id)
                db.session.add(experience)
            else:
                if viewing_status is None:
                    db.session.delete(experience)
                    db.session.commit()
                    return jsonify({"success": True})

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

        @app.route("/api/clear_all/<int:year>", methods=["POST"])
        def clear_all_year(year):
            performances = Performance.query.filter_by(year=year).all()
            for perf in performances:
                experience = Experience.query.filter_by(user_id=USER_ID, performance_id=perf.id).first()
                if experience:
                    db.session.delete(experience)
            db.session.commit()
            return jsonify({"success": True})

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
