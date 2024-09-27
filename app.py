from flask import Flask, render_template
from database import get_statistics

app = Flask(__name__)

@app.route('/')
def index():
    weekly_users = get_statistics('week')
    monthly_users = get_statistics('month')
    return render_template('index.html', weekly_users=weekly_users, monthly_users=monthly_users)

if __name__ == '__main__':
    app.run(debug=True)
