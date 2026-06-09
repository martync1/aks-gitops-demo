from flask import Flask, render_template, request, redirect, url_for
import pymysql
import os

app = Flask(__name__)

# Database configurations matching your live MySQL setup
DB_HOST = "my-release-mysql"
DB_USER = "root"
DB_PASSWORD = "VotingAppPass123!"
DB_NAME = "voting_db"

def get_db_connection():
    return pymysql.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        cursorclass=pymysql.cursors.DictCursor
    )

# Automatically initialize the database table on launch
def init_db():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            # Create a table to track choices if it doesn't exist
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS votes (
                    candidate VARCHAR(50) PRIMARY KEY,
                    count INT DEFAULT 0
                )
            """)
            # Initialize with default entries if empty
            cursor.execute("INSERT IGNORE INTO votes (candidate, count) VALUES ('Cats', 0), ('Dogs', 0)")
        connection.commit()
    finally:
        connection.close()

@app.route("/", methods=["GET", "POST"])
def index():
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            if request.method == "POST":
                vote = request.form.get("vote")
                if vote in ["Cats", "Dogs"]:
                    # Increment the vote count in MySQL
                    cursor.execute("UPDATE votes SET count = count + 1 WHERE candidate = %s", (vote,))
                    connection.commit()
                return redirect(url_for("index"))

            # Retrieve current standings to display
            cursor.execute("SELECT * FROM votes")
            results = cursor.fetchall()
            votes_data = {row["candidate"]: row["count"] for row in results}
    finally:
        connection.close()

    return render_template("index.html", votes=votes_data)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=8081, debug=True)
