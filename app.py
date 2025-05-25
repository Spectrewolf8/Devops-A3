from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key-here"

# Database configuration
DATABASE = "users.db"


def init_db():
    """Initialize the database with users table"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    )
    conn.commit()
    conn.close()


def get_db_connection():
    """Get database connection"""
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.route("/")
def index():
    """Home page showing all users"""
    conn = get_db_connection()
    users = conn.execute("SELECT * FROM users ORDER BY created_at DESC").fetchall()
    conn.close()
    return render_template("index.html", users=users)


@app.route("/add_user", methods=["GET", "POST"])
def add_user():
    """Add a new user"""
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]

        if not name or not email:
            flash("Name and email are required!")
            return redirect(url_for("add_user"))

        try:
            conn = get_db_connection()
            conn.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
            conn.commit()
            conn.close()
            flash("User added successfully!")
            return redirect(url_for("index"))
        except sqlite3.IntegrityError:
            flash("Email already exists!")
            return redirect(url_for("add_user"))

    return render_template("add_user.html")


@app.route("/delete_user/<int:user_id>")
def delete_user(user_id):
    """Delete a user"""
    conn = get_db_connection()
    conn.execute("DELETE FROM users WHERE id = ?", (user_id,))
    conn.commit()
    conn.close()
    flash("User deleted successfully!")
    return redirect(url_for("index"))


@app.route("/health")
def health_check():
    """Health check endpoint for testing"""
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    init_db()
    app.run(debug=True, host="0.0.0.0", port=5000)
