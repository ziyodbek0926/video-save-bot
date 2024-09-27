from flask import Flask, render_template
from database import get_statistics

app = Flask(__name__)

@app.route('/')
def index():
    try:
        weekly_users = get_statistics('week')
        monthly_users = get_statistics('month')
    except Exception as e:
        # Xato yuz berishi holatida
        print(f"Xato: {e}")
        weekly_users = 0
        monthly_users = 0
    
    return render_template('index.html', weekly_users=weekly_users, monthly_users=monthly_users)

if __name__ == '__main__':
    app.run(debug=True)
