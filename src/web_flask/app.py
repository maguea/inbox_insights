# tolu kolade

from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    # Check if user is logged in using your existing functions
    if False:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/config')
def client_settings():
    return render_template('settings.html')

@app.route('/history')
def view_all_emails():
    return render_template('history.html')


if __name__ == '__main__':
    app.run(port=6222, debug=True)