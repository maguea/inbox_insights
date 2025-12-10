from flask import render_template, request, jsonify, session

from src.lib.account.user_accounts import _user_create_account
from . import bp_login

@bp_login.get("/login")
def login_page():
    return render_template('login_page.html')

# this is implemented in api.check_user. should be moved here
@bp_login.post('/login')
def email_login():
    # username = request.form.get('user')
    # server = request.form.get('server')

    # if not username or not server:
    #     return jsonify({'ok': False, 'msg': 'Missing user/server'}), 400


    # res = _email_login(username, server)
    # if res == EMAIL_CONST.IMAP_CONN_FAIL:
    #     return jsonify({'ok': False, 'msg': 'Email login failed'}), 401

    # session['email_user'] = username
    # session['email_server'] = server
    return jsonify({'ok': False, 'msg': 'not implemented'})

@bp_login.post("/new_acc")
def login_submit():
    username = request.form.get('username')
    password = request.form.get('password')
    session['email_server'] = request.form.get('server')
    print(f'{username}, {password}')
    # db find if valid user/credentials
    _user_create_account(user=username, password=password)
    # return code
    return jsonify({'ok': True})
