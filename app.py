# FILE: app.py
from flask import Flask, render_template, request, redirect
import psycopg2

app = Flask(__name__)

# -----------------------------
# Database connection
# -----------------------------

conn = psycopg2.connect(
    dbname="online_learning",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5433"
)

cur = conn.cursor()

# -----------------------------
# ROUTE: Homepage
# -----------------------------
@app.route("/")
def home():
    return render_template("home.html")

# -----------------------------
# ROUTE: Login
# -----------------------------
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        cur.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        user = cur.fetchone()

        if user:
            # For demo purposes, set user_id = user[0]
            global current_user_id
            current_user_id = user[0]
            return redirect("/dashboard")
        return "Invalid login"
    return render_template("login.html")

# -----------------------------
# ROUTE: Register
# -----------------------------
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Check if username exists
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        existing = cur.fetchone()
        if existing:
            return "Username already exists."

        # Insert new user
        cur.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
        conn.commit()
        return redirect("/login")
    return render_template("register.html")

# -----------------------------
# ROUTE: Dashboard
# -----------------------------
@app.route("/dashboard")
def dashboard():
    user_id = 1  # Replace with logged-in user ID logic
    # Get all lessons
    cur.execute("SELECT * FROM lessons")
    lessons = cur.fetchall()

    progress_data = []
    for lesson in lessons:
        lesson_id = lesson[0]
        # Get progress for this user and lesson
        cur.execute("SELECT completed, quiz_score FROM progress WHERE user_id=%s AND lesson_id=%s",
                    (user_id, lesson_id))
        p = cur.fetchone()
        completed = p[0] if p else False
        quiz_score = p[1] if p else 0

        progress_data.append({
            "id": lesson_id,
            "title": lesson[1],
            "video_url": lesson[2],
            "description": lesson[3],
            "completed": completed,
            "quiz_score": quiz_score,
            "progress_percent": 100 if completed else 0
        })

    return render_template("dashboard.html", lessons=progress_data)
# -----------------------------
# ROUTE: Lesson Page
# -----------------------------
@app.route("/lesson/<int:lesson_id>")
def lesson(lesson_id):
    cur.execute("SELECT * FROM lessons WHERE id=%s", (lesson_id,))
    lesson = cur.fetchone()
    return render_template("lesson.html", lesson=lesson)






# -----------------------------
# ROUTE: Quiz Page
# -----------------------------
@app.route("/quiz/<int:lesson_id>", methods=["GET", "POST"])
def quiz(lesson_id):
    user_id = 1  # Replace with logged-in user ID
    cur.execute("SELECT * FROM quizzes WHERE lesson_id=%s", (lesson_id,))
    q = cur.fetchone()

    if request.method == "POST":
        user_answer = int(request.form["answer"])
        score = 1 if user_answer == q[7] else 0

        # Save progress
        cur.execute("""
            INSERT INTO progress (user_id, lesson_id, completed, quiz_score)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (user_id, lesson_id) DO UPDATE
            SET completed=EXCLUDED.completed,
                quiz_score=EXCLUDED.quiz_score
        """, (user_id, lesson_id, True, score))
        conn.commit()

        return redirect("/dashboard")  # Go back to dashboard after submission

    return render_template("quiz.html", q=q)

# -----------------------------
# Run App
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)