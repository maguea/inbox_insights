from flask import render_template, request, jsonify
from . import bp_login

@bp_login.get("/login")
def login_page():
    return render_template('login_page.html')

@bp_login.post("/login")
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    print(f'{username}, {password}')
    # db find if valid user/credentials
    # return code
    return jsonify({'msg':0})
