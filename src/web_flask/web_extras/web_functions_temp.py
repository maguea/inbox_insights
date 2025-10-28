# tolu kolade
from flask import Flask, render_template, request, redirect, url_for, abort
from flask import jsonify, render_template

import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.lib.account.create_accounts import _create_account, _login, _check_env
from src.lib.account.categories import save_categories, load_categories
from src.web_flask.web_extras.testing_extra import SAMPLE_EMAILS

def get_error_message(result_code):
    error_messages = {
        0: 'Success',
        1: "Incorrect email or password",
        2: "Account not set up properly",
        3: "Cannot connect to IMAP server"
    }
    return error_messages.get(result_code, "Unknown error occurred")

def get_current_user():
    try:
        from dotenv import load_dotenv
        load_dotenv()
        return {
            'username': os.getenv('CLIENT_USER'),
            'password': os.getenv('CLIENT_PASS')
        }
    except:
        return None
