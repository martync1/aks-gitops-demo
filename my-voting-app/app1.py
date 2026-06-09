from flask import Flask, render_template, request
import redis

app = Flask(__name__)
db = redis.Redis(host='voting-db', port=6379)

@app.route("/", methods=['POST', 'GET'])
def vote():
    if request.method == 'POST':
        vote_choice = request.form['vote']
        db.incr(vote_choice) # Saves vote to database
    return "Voting App Frontend Live!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
