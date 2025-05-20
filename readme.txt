# Primavera Playback  
Created by Christiano Ferreira  
Live site: https://corpuschris.pythonanywhere.com  
GitHub repo: https://github.com/corpuschris/primavera-playback

---

##  What is this?

**Primavera Playback** is a personal web app I built to keep track of all the artists I’ve seen (or skipped!) at Primavera Sound from 2022 to 2025.

The idea is simple: I wanted a space where I could look back at each festival day, mark who I watched, rate those shows, and see it all visually. It’s part archive, part interactive diary — and hopefully useful for other fans too.

You can search by artist, filter by what you’ve watched or skipped, and the home page shows you a fun summary of your “festival history.”

---

##  Tech Stuff

This project was built using:

- Python with Flask (back-end)
- SQLite (database)
- HTML, CSS & JavaScript (front-end)
- Flask-SQLAlchemy for handling database models
- Hosted on PythonAnywhere

---

##  Features

- View full Primavera Sound lineups (2022–2025)
- Artists grouped by day and stage
- Mark performances as watched, glanced at, or skipped
- Rate shows as good, okay, or bad (if you watched it)
- Search and filter by artist name or status
- Animated, colour-coded “bubbles” for each act
- Home page shows your watched history, split by year

---


##  How to run it locally

1. **Clone this repository:**

    ```bash
    git clone https://github.com/corpuschris/primavera-playback.git
    cd primavera-playback
    ```

2. **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    venv\Scripts\activate  # On Windows
    # Or use: source venv/bin/activate on Mac/Linux
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

4. **Run the app:**

    ```bash
    python app.py
    ```

5. **Open your browser at:**

    ```
    http://127.0.0.1:5000
    ```

---

##  Deployed version

You can also access the app online here:  
-> https://corpuschris.pythonanywhere.com



— Christiano Ferreira