from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, login_user, login_required, logout_user, UserMixin, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from database import init_db, get_db
import sqlite3
from datetime import datetime

app = Flask(__name__)
app.secret_key = "supersecretkey"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = generate_password_hash(request.form["password"])
        role = request.form.get("role", "attendee")

        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, password, role))
            conn.commit()
            conn.close()
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("login"))
        except sqlite3.IntegrityError:
            flash("Username already exists!", "danger")

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user["password"], password):
            session["user_id"] = user["id"]
            session["username"] = user["username"]
            session["role"] = user["role"]
            flash("Login successful!", "success")
            return redirect(url_for("events"))
        else:
            flash("Invalid username or password", "danger")

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logged out successfully!", "info")
    return redirect(url_for("login"))



@app.route("/events")
def events():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM events")
    events = cursor.fetchall()
    conn.close()
    return render_template("events.html", events=events)


@app.route("/create_event", methods=["GET", "POST"])
def create_event():
    if "user_id" not in session or session["role"] != "organizer":
        flash("Only organizers can create events.", "danger")
        return redirect(url_for("events"))

    if request.method == "POST":
        title = request.form["title"]
        description = request.form["description"]
        date = datetime.strptime(request.form["date"], "%Y-%m-%dT%H:%M")
        capacity = request.form["capacity"]
        location = request.form["location"]
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO events (title, description,location, date, capacity) VALUES (?, ?, ?, ?,?)",
                       (title, description,location, date.isoformat(), capacity))
        conn.commit()
        conn.close()

        flash("Event created successfully!", "success")
        return redirect(url_for("events"))

    return render_template("create_event.html")

@app.route("/profile")
def profile():
    if "user_id" not in session:
        flash("Please log in to view your profile.")
        return redirect(url_for("login"))

    conn = get_db()
    user = conn.execute(
        "SELECT username, role FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()

    bookings = conn.execute(
        """SELECT events.title, events.location ,events.date
           FROM bookings 
           JOIN events ON bookings.event_id = events.id 
           WHERE bookings.user_id = ?""",
        (session["user_id"],)
    ).fetchall()

    conn.close()
    return render_template("profile.html", user=user, bookings=bookings)


@app.route("/edit_profile", methods=["GET", "POST"])
def edit_profile():
    if "user_id" not in session:
        flash("Please log in to edit your profile.")
        return redirect(url_for("login"))

    conn = get_db()
    user = conn.execute(
        "SELECT id, username, role FROM users WHERE id = ?", (session["user_id"],)
    ).fetchone()

    if request.method == "POST":
        new_username = request.form["username"]
        new_password = request.form["password"]

        if new_username:
            conn.execute("UPDATE users SET username = ? WHERE id = ?", (new_username, user["id"]))

        if new_password: 
            conn.execute("UPDATE users SET password = ? WHERE id = ?", (new_password, user["id"]))

        conn.commit()
        conn.close()

        flash("Profile updated successfully!")
        return redirect(url_for("profile"))

    conn.close()
    return render_template("edit_profile.html", user=user)

@app.route("/book_event/<int:event_id>")
def book_event(event_id):
    if "user_id" not in session:
        flash("Please log in to book an event.")
        return redirect(url_for("login"))

    conn = get_db()
   
    existing = conn.execute(
        "SELECT * FROM bookings WHERE user_id = ? AND event_id = ?",
        (session["user_id"], event_id)
    ).fetchone()

    if existing:
        flash("You already booked this event.")
    else:
        conn.execute(
            "INSERT INTO bookings (user_id, event_id) VALUES (?, ?)",
            (session["user_id"], event_id)
        )
        conn.commit()
        flash("Event booked successfully!")

    conn.close()
    return redirect(url_for("events"))
@app.route("/delete_event/<int:event_id>", methods=["POST"])
def delete_event(event_id):
    if session.get("role") != "organizer":  
        flash("Unauthorized action!", "danger")
        return redirect(url_for("events"))

    conn = get_db()
    cursor = conn.cursor()

   
    cursor.execute("DELETE FROM bookings WHERE event_id = ?", (event_id,))
  
    cursor.execute("DELETE FROM events WHERE id = ?", (event_id,))
    conn.commit()
    conn.close()

    flash("Event deleted successfully!", "success")
    return redirect(url_for("events"))

if __name__ == "__main__":
    init_db()  
    app.run(debug=True)